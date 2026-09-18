"""OpenMotorBridge Google Drive WebDAV Bridge.

Accepts standard WebDAV file uploads (PUT) from the OpenMotorBridge Central Box
and transparently uploads GPX tours into Google Drive, with optional MQTT / Webhook
event dispatching to Home Assistant / Homesphere.
"""

import logging
import secrets
from typing import Annotated
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import settings
from gdrive import gdrive_client
from notifier import dispatch_upload_event

# Logging configuration
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("omb.bridge")

app = FastAPI(
    title="OpenMotorBridge Google Drive WebDAV Bridge",
    description="Minimal WebDAV-to-Google-Drive upload bridge for motorcycle telemetry and GPX tracks.",
    version="1.0.0",
)

security = HTTPBasic(auto_error=False)


def authenticate(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """Verifies HTTP Basic Auth credentials from OpenMotorBridge."""
    if not settings.WEBDAV_PASSWORD:
        # Password not configured -> allow access but log warning
        return True

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": 'Basic realm="OpenMotorBridge WebDAV"'},
        )

    correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), settings.WEBDAV_USER.encode("utf8")
    )
    correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), settings.WEBDAV_PASSWORD.encode("utf8")
    )

    if not (correct_username and correct_password):
        logger.warning(f"Failed authentication attempt for user '{credentials.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": 'Basic realm="OpenMotorBridge WebDAV"'},
        )

    return True


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestrators and monitoring."""
    gdrive_ready = bool(
        settings.GOOGLE_CLIENT_ID
        and settings.GOOGLE_CLIENT_SECRET
        and settings.GOOGLE_REFRESH_TOKEN
    )
    return {
        "status": "healthy",
        "service": "omb-gdrive-bridge",
        "version": "1.0.0",
        "gdrive_ready": gdrive_ready,
        "target_folder": settings.GOOGLE_DRIVE_FOLDER,
        "mqtt_enabled": settings.MQTT_ENABLED or bool(settings.MQTT_BROKER),
    }


@app.get("/")
async def root_info():
    """Information endpoint."""
    return {
        "message": "OpenMotorBridge Google Drive WebDAV Bridge is running.",
        "webdav_endpoint": "/tracks/",
        "docs": "/docs",
    }


# ==============================================================================
# WEBDAV RFC 4918 HANDLERS
# ==============================================================================

@app.api_route("/tracks/{filename:path}", methods=["OPTIONS"], include_in_schema=False)
@app.api_route("/tracks", methods=["OPTIONS"], include_in_schema=False)
@app.api_route("/{filename:path}", methods=["OPTIONS"], include_in_schema=False)
async def webdav_options(request: Request):
    """Responds to WebDAV OPTIONS queries confirming DAV Level 1 compliance."""
    headers = {
        "DAV": "1",
        "Allow": "OPTIONS, GET, HEAD, PUT, MKCOL, PROPFIND",
        "MS-Author-Via": "DAV",
    }
    return Response(content="", status_code=status.HTTP_200_OK, headers=headers)


@app.api_route("/tracks/{folder:path}", methods=["MKCOL"], include_in_schema=False)
@app.api_route("/tracks", methods=["MKCOL"], include_in_schema=False)
@app.api_route("/{folder:path}", methods=["MKCOL"], include_in_schema=False)
async def webdav_mkcol(
    request: Request,
    folder: str = "tracks",
    auth: bool = Depends(authenticate),
):
    """WebDAV MKCOL: Idempotent collection creation (returns 201 Created)."""
    return Response(content="", status_code=status.HTTP_201_CREATED)


@app.api_route("/tracks/{path:path}", methods=["PROPFIND"], include_in_schema=False)
@app.api_route("/tracks", methods=["PROPFIND"], include_in_schema=False)
async def webdav_propfind(
    request: Request,
    auth: bool = Depends(authenticate),
):
    """Minimal WebDAV PROPFIND response so sync clients discover collection."""
    xml_response = """<?xml version="1.0" encoding="utf-8" ?>
<D:multistatus xmlns:D="DAV:">
  <D:response>
    <D:href>/tracks/</D:href>
    <D:propstat>
      <D:prop>
        <D:resourcetype><D:collection/></D:resourcetype>
      </D:prop>
      <D:status>HTTP/1.1 200 OK</D:status>
    </D:propstat>
  </D:response>
</D:multistatus>"""
    return Response(
        content=xml_response,
        status_code=status.HTTP_207_MULTI_STATUS,
        media_type="application/xml; charset=utf-8",
    )


@app.api_route("/tracks/{filename:path}", methods=["PUT"])
@app.api_route("/{filename:path}", methods=["PUT"])
async def webdav_put(
    filename: str,
    request: Request,
    background_tasks: BackgroundTasks,
    auth: bool = Depends(authenticate),
):
    """Core WebDAV PUT handler: Receives GPX file from OpenMotorBridge and uploads to Google Drive."""
    # Sanitize filename
    clean_filename = filename.strip("/").split("/")[-1]
    if not clean_filename:
        clean_filename = "unnamed_tour.gpx"

    body = await request.body()
    if not body:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file body received",
        )

    mime_type = request.headers.get("content-type", "application/gpx+xml")
    logger.info(f"Incoming WebDAV PUT: '{clean_filename}' ({len(body)} bytes, {mime_type})")

    try:
        # Upload to Google Drive
        file_info = await gdrive_client.upload_file(clean_filename, body, mime_type)
    except Exception as e:
        logger.exception(f"Failed to upload '{clean_filename}' to Google Drive: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Google Drive upload failed: {str(e)}",
        )

    # Trigger optional notifications in background task
    background_tasks.add_task(dispatch_upload_event, clean_filename, file_info, body)

    response_headers = {
        "Location": f"/tracks/{clean_filename}",
        "ETag": f'"{file_info.get("id", "gdrive")}"',
    }

    return Response(
        content=f'{{"status":"created","file_id":"{file_info.get("id")}","name":"{clean_filename}"}}\n',
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
        headers=response_headers,
    )
