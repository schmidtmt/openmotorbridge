#!/bin/bash
set -e

# ==============================================================================
# OpenMotorBridge Companion App - Build & Deployment Script
# ==============================================================================
# Automatisiert:
# 1. Versions-Inkrementierung (pubspec.yaml) vor jedem Build
# 2. Flutter APK Kompilierung (Release Mode)
# 3. Optional: iOS Bundle / Unsigned IPA für SideStore / AltStore
# 4. Erstellung der Update-Manifeste (version.json & apps.json)
# 5. Staging im lokalen dist/ Ordner
# 6. Bereitstellung in Google Drive (sofern vorhanden)
# 7. Bereitstellung per SCP auf dem lokalen Server / Raspberry Pi
# 8. Optional: Git-Tagging
# ==============================================================================

# Farbausgabe
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verzeichnisse ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/../pubspec.yaml" ]; then
    APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
    REPO_ROOT="$(cd "$APP_DIR/../.." && pwd)"
elif [ -f "$SCRIPT_DIR/../apps/omb_companion/pubspec.yaml" ]; then
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    APP_DIR="$REPO_ROOT/apps/omb_companion"
else
    REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    APP_DIR="$REPO_ROOT/apps/omb_companion"
fi

PUBSPEC="$APP_DIR/pubspec.yaml"
DIST_DIR="$APP_DIR/dist"

if [ ! -f "$PUBSPEC" ]; then
    echo -e "${RED}❌ Fehler: pubspec.yaml nicht gefunden unter $PUBSPEC${NC}"
    exit 1
fi

# Flutter Binary suchen
FLUTTER_BIN="$(which flutter 2>/dev/null || echo "$HOME/flutter/bin/flutter")"
if [ ! -x "$FLUTTER_BIN" ]; then
    echo -e "${RED}❌ Fehler: Flutter Executable nicht gefunden!${NC}"
    exit 1
fi

# Standardeinstellungen & Optionen
BUMP_VERSION=true
BUMP_TYPE="auto" # auto (homesphere style), patch, minor, major
BUILD_IOS=false
DEPLOY_REMOTE=false
DO_GIT_TAG=false

# Deployment-Ziele (Konfigurierbar über Umgebungsvariablen)
GDRIVE_BASE="/Users/schmidtm/Library/CloudStorage/GoogleDrive-mail.mts@gmail.com/Meine Ablage"
GDRIVE_PATH="${OMB_GDRIVE_PATH:-$GDRIVE_BASE/OpenMotorBridge/app}"
PI_HOST="${OMB_DEPLOY_HOST:-${PI_HOST:-homesphere.f0o.bar}}"
PI_USER="${OMB_DEPLOY_USER:-${PI_USER:-schmidtm}}"
PI_DEST="${OMB_DEPLOY_DEST:-/home/schmidtm/homesphere/api-service/data}"

# Parameter parsen
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-bump)
            BUMP_VERSION=false
            shift
            ;;
        --patch)
            BUMP_TYPE="patch"
            shift
            ;;
        --minor)
            BUMP_TYPE="minor"
            shift
            ;;
        --major)
            BUMP_TYPE="major"
            shift
            ;;
        --ios)
            BUILD_IOS=true
            shift
            ;;
        --remote)
            DEPLOY_REMOTE=true
            shift
            ;;
        --tag)
            DO_GIT_TAG=true
            shift
            ;;
        -h|--help)
            echo "Verwendung: $0 [OPTIONEN]"
            echo ""
            echo "Optionen:"
            echo "  --no-bump    Version in pubspec.yaml nicht verändern"
            echo "  --patch      Explizit Patch-Version inkrementieren (z. B. 1.0.1 ➔ 1.0.2)"
            echo "  --minor      Minor-Version inkrementieren (z. B. 1.0.x ➔ 1.1.0)"
            echo "  --major      Major-Version inkrementieren (z. B. 1.x.x ➔ 2.0.0)"
            echo "  --ios        Zusätzlich iOS Runner & unsigned IPA bauen (auf macOS)"
            echo "  --remote     SCP-Upload auf Server/Pi ($PI_HOST) erzwingen"
            echo "  --tag        Git-Release-Tag automatisch erstellen und pushen"
            echo "  -h, --help   Diese Hilfe anzeigen"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Unbekannte Option: $1${NC}"
            shift
            ;;
    esac
done

echo -e "${CYAN}======================================================${NC}"
echo -e "${CYAN}🚀 OpenMotorBridge Companion - Build & Deploy Pipeline${NC}"
echo -e "${CYAN}======================================================${NC}"

# ------------------------------------------------------------------------------
# 1. Version auslesen & automatisch inkrementieren
# ------------------------------------------------------------------------------
VERSION_LINE=$(grep '^version: ' "$PUBSPEC")
RAW_VERSION=$(echo "$VERSION_LINE" | awk '{print $2}')

if [ -z "$RAW_VERSION" ]; then
    echo -e "${RED}❌ Konnte Versionszeile in $PUBSPEC nicht finden!${NC}"
    exit 1
fi

SEMVER=$(echo "$RAW_VERSION" | cut -d'+' -f1)
OLD_CODE=$(echo "$RAW_VERSION" | cut -d'+' -f2)
[ -z "$OLD_CODE" ] && OLD_CODE=0

MAJOR=$(echo "$SEMVER" | cut -d'.' -f1)
MINOR=$(echo "$SEMVER" | cut -d'.' -f2)
PATCH=$(echo "$SEMVER" | cut -d'.' -f3)

[ -z "$MAJOR" ] && MAJOR=1
[ -z "$MINOR" ] && MINOR=0
[ -z "$PATCH" ] && PATCH=0

if [ "$BUMP_VERSION" = true ]; then
    NEW_CODE=$((OLD_CODE + 1))
    
    if [ "$BUMP_TYPE" = "auto" ]; then
        # HomeSphere Pattern: Major.Minor.NewCode+NewCode
        NEW_VERSION="${MAJOR}.${MINOR}.${NEW_CODE}+${NEW_CODE}"
        VERSION_NAME="${MAJOR}.${MINOR}.${NEW_CODE}"
    elif [ "$BUMP_TYPE" = "patch" ]; then
        NEW_PATCH=$((PATCH + 1))
        NEW_VERSION="${MAJOR}.${MINOR}.${NEW_PATCH}+${NEW_CODE}"
        VERSION_NAME="${MAJOR}.${MINOR}.${NEW_PATCH}"
    elif [ "$BUMP_TYPE" = "minor" ]; then
        NEW_MINOR=$((MINOR + 1))
        NEW_VERSION="${MAJOR}.${NEW_MINOR}.0+${NEW_CODE}"
        VERSION_NAME="${MAJOR}.${NEW_MINOR}.0"
    elif [ "$BUMP_TYPE" = "major" ]; then
        NEW_MAJOR=$((MAJOR + 1))
        NEW_VERSION="${NEW_MAJOR}.0.0+${NEW_CODE}"
        VERSION_NAME="${NEW_MAJOR}.0.0"
    fi
    VERSION_CODE="${NEW_CODE}"
    
    echo -e "${GREEN}🔄 Automatisches Inkrementieren der Version:${NC} $RAW_VERSION ➔ ${YELLOW}$NEW_VERSION${NC}"
    
    # In pubspec.yaml ersetzen (OSX sed vs. Linux sed kompatibel)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^version: .*/version: $NEW_VERSION/" "$PUBSPEC"
    else
        sed -i "s/^version: .*/version: $NEW_VERSION/" "$PUBSPEC"
    fi
else
    NEW_VERSION="$RAW_VERSION"
    VERSION_NAME="$SEMVER"
    VERSION_CODE="$OLD_CODE"
    echo -e "${YELLOW}ℹ️  Verwende existierende Version ohne Erhöhung:${NC} $NEW_VERSION"
fi

FILE_VERSION="${VERSION_NAME}-${VERSION_CODE}"
echo -e "${GREEN}ℹ️  App-Version für diesen Build:${NC} $VERSION_NAME (Build-Code: $VERSION_CODE)"

# ------------------------------------------------------------------------------
# 2. Flutter Build vorbereiten & säubern
# ------------------------------------------------------------------------------
cd "$APP_DIR"
echo -e "\n${CYAN}🧹 Säubere temporäre Build-Dateien...${NC}"
rm -rf "$APP_DIR/build/app" "$APP_DIR/build/ios/ipa" "$APP_DIR/build/ios/iphoneos"
mkdir -p "$DIST_DIR"

echo -e "${CYAN}📦 Hole Flutter Abhängigkeiten...${NC}"
"$FLUTTER_BIN" pub get

# ------------------------------------------------------------------------------
# 3. Android APK Release bauen
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}📦 Kompiliere Android Release APK (bar.f0o.omb)...${NC}"
"$FLUTTER_BIN" build apk --release

APK_SOURCE="$APP_DIR/build/app/outputs/flutter-apk/app-release.apk"
if [ ! -f "$APK_SOURCE" ]; then
    echo -e "${RED}❌ Fehler: APK wurde nicht generiert unter $APK_SOURCE${NC}"
    exit 1
fi
echo -e "${GREEN}✅ APK erfolgreich kompiliert:${NC} $(ls -lh "$APK_SOURCE" | awk '{print $5}')"

# ------------------------------------------------------------------------------
# 4. Optional: iOS Bundle & Unsigned IPA (SideStore / AltStore)
# ------------------------------------------------------------------------------
IPA_SOURCE=""
if [ "$BUILD_IOS" = true ] && [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "\n${CYAN}📦 Kompiliere iOS App (No-Codesign Mode)...${NC}"
    "$FLUTTER_BIN" build ios --no-codesign --release || true
    
    RUNNER_APP="$APP_DIR/build/ios/iphoneos/Runner.app"
    if [ -d "$RUNNER_APP" ]; then
        echo -e "${CYAN}📦 Verpacke iOS App als unsigned IPA für SideStore / AltStore...${NC}"
        rm -rf "$APP_DIR/build/ios/ipa"
        mkdir -p "$APP_DIR/build/ios/ipa/Payload"
        cp -r "$RUNNER_APP" "$APP_DIR/build/ios/ipa/Payload/"
        (cd "$APP_DIR/build/ios/ipa" && zip -r -q "openmotorbridge.ipa" Payload)
        IPA_SOURCE="$APP_DIR/build/ios/ipa/openmotorbridge.ipa"
        echo -e "${GREEN}✅ IPA erfolgreich verpackt:${NC} $(ls -lh "$IPA_SOURCE" | awk '{print $5}')"
    fi
fi

# ------------------------------------------------------------------------------
# 5. Staging im lokalen dist/ Ordner
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}📋 Kopiere Artefakte in das Staging-Verzeichnis ($DIST_DIR)...${NC}"
cp "$APK_SOURCE" "$DIST_DIR/openmotorbridge-release.apk"
cp "$APK_SOURCE" "$DIST_DIR/openmotorbridge-${FILE_VERSION}.apk"

if [ -n "$IPA_SOURCE" ] && [ -f "$IPA_SOURCE" ]; then
    cp "$IPA_SOURCE" "$DIST_DIR/openmotorbridge-release.ipa"
    cp "$IPA_SOURCE" "$DIST_DIR/openmotorbridge-${FILE_VERSION}.ipa"
fi

if [ -f "$APP_DIR/assets/images/logo.jpg" ]; then
    cp "$APP_DIR/assets/images/logo.jpg" "$DIST_DIR/logo.jpg"
fi

# Manifests generieren (version.json für In-App Self-Update)
TODAY=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat <<EOF > "$DIST_DIR/version.json"
{
  "version": "$FILE_VERSION",
  "versionName": "$VERSION_NAME",
  "buildNumber": $VERSION_CODE,
  "releaseDate": "$TODAY",
  "url": "openmotorbridge-release.apk",
  "apkFilename": "openmotorbridge-${FILE_VERSION}.apk",
  "notes": "OpenMotorBridge Companion App v$VERSION_NAME (Build $VERSION_CODE)"
}
EOF

# Manifest für SideStore / AltStore
cat <<EOF > "$DIST_DIR/apps.json"
{
  "name": "OpenMotorBridge Source",
  "identifier": "bar.f0o.omb.source",
  "iconURL": "https://homesphere.f0o.bar:8443/homesphere-api/static/omb_logo.jpg",
  "website": "https://github.com/schmidtmt/openmotorbridge",
  "apps": [
    {
      "name": "OMB Companion",
      "bundleIdentifier": "bar.f0o.omb",
      "developerName": "OpenMotorBridge",
      "subtitle": "Cellular Proxy & GNSS BLE Bridge",
      "localizedDescription": "OpenMotorBridge Companion App with Layer-5 Cellular SOCKS5 Proxy and AssistNow GNSS Injection",
      "iconURL": "https://homesphere.f0o.bar:8443/homesphere-api/static/omb_logo.jpg",
      "tintColor": "00F2FE",
      "versions": [
        {
          "version": "${VERSION_NAME}",
          "date": "${TODAY}",
          "downloadURL": "https://homesphere.f0o.bar:8443/homesphere-api/static/openmotorbridge-release.ipa"
        }
      ]
    }
  ]
}
EOF

echo -e "${GREEN}✅ Lokales Staging abgeschlossen:${NC}"
ls -lh "$DIST_DIR"

# ------------------------------------------------------------------------------
# 6. Bereitstellung in Google Drive (falls Pfad verfügbar)
# ------------------------------------------------------------------------------
if [ -d "$(dirname "$GDRIVE_PATH")" ]; then
    echo -e "\n${CYAN}📤 Bereitstellung in Google Drive ($GDRIVE_PATH)...${NC}"
    mkdir -p "$GDRIVE_PATH"
    cp "$DIST_DIR/openmotorbridge-release.apk" "$GDRIVE_PATH/"
    cp "$DIST_DIR/openmotorbridge-${FILE_VERSION}.apk" "$GDRIVE_PATH/"
    cp "$DIST_DIR/version.json" "$GDRIVE_PATH/"
    if [ -f "$DIST_DIR/openmotorbridge-release.ipa" ]; then
        cp "$DIST_DIR/openmotorbridge-release.ipa" "$GDRIVE_PATH/"
        cp "$DIST_DIR/openmotorbridge-${FILE_VERSION}.ipa" "$GDRIVE_PATH/"
    fi
    echo -e "${GREEN}🎉 Erfolgreich ins Google Drive übertragen!${NC}"
fi

# ------------------------------------------------------------------------------
# 7. Bereitstellung auf dem lokalen Server / Raspberry Pi (per SCP)
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}🌐 Prüfe Verfügbarkeit des lokalen Update-Servers ($PI_HOST)...${NC}"
SERVER_REACHABLE=false
if nc -z -G 2 "$PI_HOST" 22 2>/dev/null; then
    SERVER_REACHABLE=true
elif ping -c 1 -W 2 "$PI_HOST" >/dev/null 2>&1; then
    SERVER_REACHABLE=true
fi

if [ "$SERVER_REACHABLE" = true ] || [ "$DEPLOY_REMOTE" = true ]; then
    echo -e "${CYAN}📤 Übertrage APK, version.json und Metadaten per SCP auf $PI_HOST...${NC}"
    set +e
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/openmotorbridge-release.apk" "${PI_USER}@${PI_HOST}:${PI_DEST}/static/openmotorbridge-release.apk"
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/openmotorbridge-${FILE_VERSION}.apk" "${PI_USER}@${PI_HOST}:${PI_DEST}/static/openmotorbridge-${FILE_VERSION}.apk"
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/version.json" "${PI_USER}@${PI_HOST}:${PI_DEST}/static/omb_version.json"
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/version.json" "${PI_USER}@${PI_HOST}:${PI_DEST}/version.json"
    scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/apps.json" "${PI_USER}@${PI_HOST}:${PI_DEST}/static/omb_apps.json"
    if [ -f "$DIST_DIR/logo.jpg" ]; then
        scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/logo.jpg" "${PI_USER}@${PI_HOST}:${PI_DEST}/static/omb_logo.jpg"
    fi
    if [ -f "$DIST_DIR/openmotorbridge-release.ipa" ]; then
        scp -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$DIST_DIR/openmotorbridge-release.ipa" "${PI_USER}@${PI_HOST}:${PI_DEST}/static/openmotorbridge-release.ipa"
    fi
    SCP_STATUS=$?
    set -e
    if [ $SCP_STATUS -eq 0 ]; then
        echo -e "${GREEN}🎉 Erfolgreich auf den Raspberry Pi / Update-Server übertragen!${NC}"
    else
        echo -e "${YELLOW}⚠️  Hinweis: SCP-Übertragung konnte nicht vollständig abgeschlossen werden.${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  Server $PI_HOST im aktuellen Netzwerk nicht erreichbar.${NC}"
    echo -e "   Dateien liegen bereit in: $DIST_DIR"
    echo -e "   Sobald du mit dem Heimnetz/Tailscale verbunden bist, kannst du mit '--remote' synchronisieren."
fi

# ------------------------------------------------------------------------------
# 8. Git-Tagging (optional)
# ------------------------------------------------------------------------------
if [ "$DO_GIT_TAG" = true ]; then
    TAG_NAME="v$FILE_VERSION"
    echo -e "\n${CYAN}🏷️  Erstelle Git-Tag $TAG_NAME...${NC}"
    if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
        echo -e "${YELLOW}ℹ️  Git-Tag $TAG_NAME existiert bereits.${NC}"
    else
        git tag -a "$TAG_NAME" -m "OpenMotorBridge Companion Release $TAG_NAME"
        git push origin "$TAG_NAME" || echo -e "${YELLOW}⚠️  Konnte Git-Tag nicht zu origin pushen.${NC}"
        echo -e "${GREEN}🎉 Git-Tag $TAG_NAME erfolgreich erstellt!${NC}"
    fi
fi

echo -e "\n${GREEN}======================================================${NC}"
echo -e "${GREEN}✅ Build & Bereitstellung erfolgreich abgeschlossen!${NC}"
echo -e "${GREEN}   Version:       v$VERSION_NAME (Build $VERSION_CODE)${NC}"
echo -e "${GREEN}   Release-APK:   $DIST_DIR/openmotorbridge-release.apk${NC}"
echo -e "${GREEN}   Manifest:      $DIST_DIR/version.json${NC}"
echo -e "${GREEN}======================================================${NC}"
