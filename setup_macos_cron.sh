#!/bin/bash
# Installs a macOS LaunchAgent to automatically execute local_runner.sh every day at 12:00 PM

PLIST_NAME="com.umut.gitbot.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p "$HOME/Library/LaunchAgents"

cat << PLIST > "$PLIST_DEST"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.umut.gitbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$PROJECT_DIR/local_runner.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>12</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/gitbot.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/gitbot_error.log</string>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
PLIST

# Unload previous instance if loaded
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"

echo "✅ LaunchAgent installed and loaded successfully at $PLIST_DEST"
echo "It will run daily at 12:00 PM."
