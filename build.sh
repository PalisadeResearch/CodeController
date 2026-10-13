#!/bin/bash

# Do not package stale output or report success after a failed build step.
set -euo pipefail

# Compile Swift to executable
swiftc CodeController.swift -o CodeController

# Create .app bundle structure
mkdir -p CodeController.app/Contents/MacOS
mkdir -p CodeController.app/Contents/Resources
mv CodeController CodeController.app/Contents/MacOS/
cp icon.png CodeController.app/Contents/Resources/
cp icon.icns CodeController.app/Contents/Resources/
cp README.md CodeController.app/Contents/Resources/
cp marked.min.js CodeController.app/Contents/Resources/
cp readme_template.html CodeController.app/Contents/Resources/
cp codecontroller_triggers.bttpreset CodeController.app/Contents/Resources/

# Create Info.plist
cat > CodeController.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>CodeController</string>
    <key>CFBundleIdentifier</key>
    <string>com.local.codecontroller</string>
    <key>CFBundleName</key>
    <string>CodeController</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>CFBundleIconFile</key>
    <string>icon</string>
    <key>LSUIElement</key>
    <true/>
</dict>
</plist>
EOF

echo "Built CodeController.app"
echo "Move it to /Applications, run it, then grant Accessibility to just that app"
