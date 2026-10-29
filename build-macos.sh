#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

.venv/bin/pyinstaller --noconfirm PromptMaster.spec
APP="dist/Prompt Master.app"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources/bridge"
cp dist/PromptMaster.app/Contents/Info.plist "$APP/Contents/Info.plist"
swiftc -O PromptMasterApp.swift -o "$APP/Contents/MacOS/PromptMaster"
cp dist/PromptMaster "$APP/Contents/Resources/bridge/PromptMaster"
cp PromptMaster.icns "$APP/Contents/Resources/PromptMaster.icns"
/usr/libexec/PlistBuddy -c 'Add :CFBundleExecutable string PromptMaster' "$APP/Contents/Info.plist" 2>/dev/null || true
/usr/libexec/PlistBuddy -c 'Set :CFBundleExecutable PromptMaster' "$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c 'Add :NSAppTransportSecurity dict' "$APP/Contents/Info.plist" 2>/dev/null || true
/usr/libexec/PlistBuddy -c 'Add :NSAppTransportSecurity:NSAllowsLocalNetworking bool true' "$APP/Contents/Info.plist" 2>/dev/null || /usr/libexec/PlistBuddy -c 'Set :NSAppTransportSecurity:NSAllowsLocalNetworking true' "$APP/Contents/Info.plist"
STAGING="$(mktemp -d)"
trap 'rm -r "$STAGING"' EXIT
ditto "$APP" "$STAGING/Prompt Master.app"
xattr -cr "$STAGING/Prompt Master.app"
codesign --force --deep --sign - "$STAGING/Prompt Master.app"
codesign --verify --deep --strict "$STAGING/Prompt Master.app"
ditto "$STAGING/Prompt Master.app" "$APP"
xattr -cr "$APP"
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"
ditto -c -k --sequesterRsrc --keepParent "$STAGING/Prompt Master.app" "dist/Prompt-Master-macOS-arm64.zip"
echo "$APP"
