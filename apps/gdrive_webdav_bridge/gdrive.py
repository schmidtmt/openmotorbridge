"""Google Drive API v3 async client for OpenMotorBridge.

Handles OAuth2 token refresh, folder traversal/creation, and multipart file uploads
without requiring large external SDK dependencies.
"""

import json
import logging
import time
from typing import Any, Dict, Optional
import httpx

from config import settings

logger = logging.getLogger("omb.gdrive")

TOKEN_URL = "https://oauth2.googleapis.com/token"
DRIVE_API_BASE = "https://www.googleapis.com/drive/v3"
DRIVE_UPLOAD_BASE = "https://www.googleapis.com/upload/drive/v3"


class GoogleDriveClient:
    def __init__(self):
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0.0
        self._folder_cache: Dict[str, str] = {}  # "omb/tracks" -> folder_id

    async def get_valid_access_token(self) -> str:
        """Returns a valid access token, automatically refreshing it if expired."""
        now = time.time()
        if self._access_token and (self._token_expiry - now) > 60:
            return self._access_token

        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET or not settings.GOOGLE_REFRESH_TOKEN:
            raise ValueError(
                "Google Drive OAuth2 credentials not fully configured. "
                "Ensure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN are set."
            )

        logger.info("Refreshing Google Drive OAuth2 access token...")
        payload = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "refresh_token": settings.GOOGLE_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(TOKEN_URL, data=payload)
            if resp.status_code != 200:
                logger.error(f"Failed to refresh Google OAuth token: {resp.status_code} - {resp.text}")
                resp.raise_for_status()

            data = resp.json()
            self._access_token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self._token_expiry = now + expires_in
            logger.info(f"Access token refreshed successfully. Valid for {expires_in}s.")
            return self._access_token

    async def ensure_folder_exists(self, folder_path: str) -> str:
        """Recursively checks or creates folder path in Google Drive (e.g. 'omb/tracks').

        Returns the folder ID of the leaf folder.
        """
        clean_path = folder_path.strip("/")
        if clean_path in self._folder_cache:
            return self._folder_cache[clean_path]

        segments = [s for s in clean_path.split("/") if s]
        if not segments:
            return "root"

        token = await self.get_valid_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        current_parent_id = "root"
        accumulated_path = []

        async with httpx.AsyncClient(timeout=20.0) as client:
            for segment in segments:
                accumulated_path.append(segment)
                current_path_str = "/".join(accumulated_path)

                if current_path_str in self._folder_cache:
                    current_parent_id = self._folder_cache[current_path_str]
                    continue

                # Search if folder already exists under current_parent_id
                query = (
                    f"name = '{segment}' and "
                    f"mimeType = 'application/vnd.google-apps.folder' and "
                    f"'{current_parent_id}' in parents and "
                    f"trashed = false"
                )
                search_url = f"{DRIVE_API_BASE}/files"
                params = {"q": query, "fields": "files(id, name)", "spaces": "drive"}

                search_resp = await client.get(search_url, headers=headers, params=params)
                if search_resp.status_code != 200:
                    logger.error(
                        f"Google Drive search error ({search_resp.status_code}) for '{segment}': {search_resp.text}"
                    )
                search_resp.raise_for_status()
                files = search_resp.json().get("files", [])

                if files:
                    folder_id = files[0]["id"]
                    logger.debug(f"Found existing Drive folder '{segment}' -> ID: {folder_id}")
                else:
                    # Create folder
                    logger.info(f"Creating Drive folder '{segment}' under parent '{current_parent_id}'...")
                    create_payload = {
                        "name": segment,
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": [current_parent_id],
                    }
                    create_resp = await client.post(
                        f"{DRIVE_API_BASE}/files",
                        headers=headers,
                        json=create_payload,
                    )
                    if create_resp.status_code not in (200, 201):
                        logger.error(
                            f"Google Drive folder create error ({create_resp.status_code}) for '{segment}': {create_resp.text}"
                        )
                    create_resp.raise_for_status()
                    folder_id = create_resp.json()["id"]
                    logger.info(f"Created folder '{segment}' -> ID: {folder_id}")

                self._folder_cache[current_path_str] = folder_id
                current_parent_id = folder_id

        return current_parent_id

    async def upload_file(
        self,
        filename: str,
        content: bytes,
        mime_type: str = "application/gpx+xml",
    ) -> Dict[str, Any]:
        """Uploads a file to the configured Google Drive folder using multipart upload."""
        token = await self.get_valid_access_token()
        folder_id = await self.ensure_folder_exists(settings.GOOGLE_DRIVE_FOLDER)

        logger.info(f"Uploading '{filename}' ({len(content)} bytes) to Drive folder '{settings.GOOGLE_DRIVE_FOLDER}' (ID: {folder_id})...")

        metadata = {
            "name": filename,
            "parents": [folder_id],
        }

        boundary = "omb_boundary_gdrive_upload"
        body = (
            f"--{boundary}\r\n"
            f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
            f"{json.dumps(metadata)}\r\n"
            f"--{boundary}\r\n"
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode("utf-8") + content + f"\r\n--{boundary}--\r\n".encode("utf-8")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        }

        upload_url = f"{DRIVE_UPLOAD_BASE}/files?uploadType=multipart&fields=id,name,size,webViewLink,createdTime"

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(upload_url, headers=headers, content=body)
            if resp.status_code not in (200, 201):
                logger.error(f"Google Drive upload failed: {resp.status_code} - {resp.text}")
                resp.raise_for_status()

            data = resp.json()
            logger.info(f"Successfully uploaded '{filename}' to Google Drive -> File ID: {data.get('id')}")
            return data


# Global singleton client
gdrive_client = GoogleDriveClient()
