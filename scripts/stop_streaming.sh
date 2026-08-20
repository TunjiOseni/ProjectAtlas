#!/bin/bash

PID=$(pgrep -f "streaming/streaming_job.py")

if [ -z "$PID" ]; then
    echo "ProjectAtlas streaming job is not running."
    exit 0
fi

echo "Stopping ProjectAtlas streaming job: $PID"

kill "$PID"

sleep 2

if pgrep -f "streaming/streaming_job.py" > /dev/null; then
    echo "Process still running. Forcing shutdown..."
    pkill -9 -f "streaming/streaming_job.py"
fi

echo "ProjectAtlas streaming job stopped."
