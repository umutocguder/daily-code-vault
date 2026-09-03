#!/bin/bash
# Controller script to start, stop, and check status of the Auto-Sync daemon

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PID_FILE="$DIR/auto_sync.pid"
LOG_FILE="$DIR/auto_sync.log"

start() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "⚠️ Auto-Sync is already running with PID $(cat "$PID_FILE")"
        return
    fi
    echo "Starting Auto-Sync Watcher daemon in background..."
    nohup python3 -u "$DIR/auto_sync.py" >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "✅ Auto-Sync started (PID: $(cat "$PID_FILE")). Changes will be pushed automatically."
}

stop() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        PID=$(cat "$PID_FILE")
        kill "$PID"
        rm -f "$PID_FILE"
        echo "🛑 Auto-Sync stopped (PID: $PID)"
    else
        echo "ℹ️ Auto-Sync is not running."
        rm -f "$PID_FILE"
    fi
}

status() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "🟢 Auto-Sync is RUNNING (PID: $(cat "$PID_FILE"))"
        echo "--- Recent Logs ---"
        tail -n 10 "$LOG_FILE" 2>/dev/null || echo "No logs yet."
    else
        echo "🔴 Auto-Sync is STOPPED."
    fi
}

sync_now() {
    echo "⚡ Triggering immediate sync..."
    python3 -u "$DIR/auto_sync.py" --once
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    status)
        status
        ;;
    sync-now)
        sync_now
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|sync-now}"
        exit 1
        ;;
esac
