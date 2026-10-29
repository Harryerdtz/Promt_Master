#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
ICONSET="PromptMaster.iconset"
mkdir -p "$ICONSET"
swift scripts/create-app-icon.swift "$ICONSET/icon_512x512@2x.png"
for size in 16 32 64 128 256 512; do
  sips -s format png -z "$size" "$size" "$ICONSET/icon_512x512@2x.png" --out "$ICONSET/icon_${size}x${size}.png" >/dev/null
done
cp "$ICONSET/icon_32x32.png" "$ICONSET/icon_16x16@2x.png"
cp "$ICONSET/icon_64x64.png" "$ICONSET/icon_32x32@2x.png"
cp "$ICONSET/icon_256x256.png" "$ICONSET/icon_128x128@2x.png"
cp "$ICONSET/icon_512x512.png" "$ICONSET/icon_256x256@2x.png"
iconutil -c icns "$ICONSET" -o PromptMaster.icns
