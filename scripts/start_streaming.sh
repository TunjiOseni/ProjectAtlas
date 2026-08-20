#!/bin/bash

set -e

PROJECT_HOME="/home/tijay/Projects/ProjectAtlas"
CLICKHOUSE_JAR="/home/tijay/insurance-etl/drivers/clickhouse-jdbc-0.9.8-all.jar"

cd "$PROJECT_HOME"

export PYTHONPATH="$PROJECT_HOME:$PYTHONPATH"

echo "Starting ProjectAtlas transaction CDC streaming..."

exec spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6 \
  --jars "$CLICKHOUSE_JAR" \
  streaming/streaming_job.py
