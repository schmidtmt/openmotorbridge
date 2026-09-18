#!/usr/bin/env python3
"""Interactive Google OAuth2 Setup Assistant for OpenMotorBridge.

Walks the user through obtaining a Google Drive refresh token for their personal
Google Cloud project and outputs the ready-to-use .env configuration.
"""

import os
import sys
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import httpx

REDIRECT_URI = "http://localhost:8085"
SCOPE = "https://www.googleapis.com/auth/drive.file"
TOKEN_URL = "https://oauth2.googleapis.com/token"

captured_code = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            captured_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<h1>Autorisierung erfolgreich!</h1>"
                b"<p>Du kannst dieses Browser-Fenster jetzt schlie&szlig;en und ins Terminal zur&uuml;ckkehren.</p>"
            )
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Fehler: Kein Autorisierungscode empfangen.")

    def log_message(self, format, *args):
        pass  # Quiet logging


def main():
    print("=" * 72)
    print("   OpenMotorBridge - Google Drive OAuth2 Setup Assistant")
    print("=" * 72)
    print()
    print("Dieser Assistent hilft dir, ein sicheres Refresh-Token für dein privates")
    print("Google Drive zu generieren. Deine Daten bleiben zu 100% bei dir.\n")

    client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip()
    if not client_id:
        client_id = input("Bitte gib deine Google Client-ID ein: ").strip()

    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip()
    if not client_secret:
        client_secret = input("Bitte gib dein Google Client-Secret ein: ").strip()

    if not client_id or not client_secret:
        print("\n[FEHLER] Client-ID und Client-Secret dürfen nicht leer sein.")
        sys.exit(1)

    auth_params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(auth_params)

    print("\n" + "-" * 72)
    print("SCHRITT 1: Autorisierung im Browser")
    print("-" * 72)
    print("Öffne folgenden Link in deinem Browser, logge dich mit deinem Google-Konto ein")
    print("und erlaube den Zugriff auf deine OpenMotorBridge-Ordner:\n")
    print(auth_url)
    print("\n" + "-" * 72)

    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    # Start local loopback server to catch code
    print("Warte auf Bestätigung im Browser (auf localhost:8085)...")
    print("(Falls dein Browser nicht automatisch weiterleitet, kannst du den Code auch manuell eingeben)")

    server = None
    try:
        server = HTTPServer(("localhost", 8085), OAuthCallbackHandler)
        server.timeout = 120
        while not captured_code:
            server.handle_request()
            if captured_code:
                break
    except Exception as e:
        print(f"\nHinweis: Lokaler Server konnte nicht gestartet werden ({e}).")

    code = captured_code
    if not code:
        code = input("\nBitte gib den 'code'-Parameter aus der URL-Adressleiste manuell ein: ").strip()

    if not code:
        print("[FEHLER] Kein Code eingegeben. Abbruch.")
        sys.exit(1)

    print("\nTausche Autorisierungscode gegen dauerhaftes Refresh-Token ein...")

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    resp = httpx.post(TOKEN_URL, data=payload)
    if resp.status_code != 200:
        print(f"\n[FEHLER] Token-Austausch fehlgeschlagen ({resp.status_code}):")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        print("\n[WARNUNG] Es wurde kein Refresh-Token zurückgegeben.")
        print("Möglicherweise war die App bereits autorisiert. Bitte führe das Skript erneut aus.")
        print("Antwort:", data)
        sys.exit(1)

    print("\n" + "=" * 72)
    print("   GLÜCKWUNSCH! REFRESH-TOKEN ERFOLGREICH ERZEUGT")
    print("=" * 72)
    print("\nFüge folgende Zeilen in deine '.env'-Datei ein:\n")
    print(f"GOOGLE_CLIENT_ID={client_id}")
    print(f"GOOGLE_CLIENT_SECRET={client_secret}")
    print(f"GOOGLE_REFRESH_TOKEN={refresh_token}")
    print("GOOGLE_DRIVE_FOLDER=omb/tracks")
    print("\n" + "=" * 72 + "\n")


if __name__ == "__main__":
    main()
