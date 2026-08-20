#!/bin/bash

echo "========================================"
echo " ProjectAtlas Health Check"
echo "========================================"

FAILED=0


# Oracle
if docker exec atlas-oracle bash -c \
  "echo 'SELECT 1 FROM dual;' | sqlplus -s banking/Banking123@localhost:1521/FREEPDB1" \
  | grep -q "1"
then
    echo "Oracle: OK"
else
    echo "Oracle: FAILED"
    FAILED=1
fi

# Debezium connector/task
STATUS=$(curl -s \
  http://localhost:8083/connectors/projectatlas-oracle-connector/status)

CONNECTOR_STATE=$(echo "$STATUS" | python -c \
'import sys,json; print(json.load(sys.stdin)["connector"]["state"])')

TASK_STATE=$(echo "$STATUS" | python -c \
'import sys,json; print(json.load(sys.stdin)["tasks"][0]["state"])')

echo "Debezium Connector: $CONNECTOR_STATE"
echo "Debezium Task:      $TASK_STATE"

# Kafka
if docker exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list | grep -q "atlas.BANKING.FACT_TRANSACTION"
then
    echo "Kafka: OK"
else
    echo "Kafka: FAILED"
    FAILED=1
fi


# Spark Streaming
if pgrep -f "streaming/streaming_job.py" > /dev/null
then
    echo "Spark Streaming: OK"
else
    echo "Spark Streaming: FAILED"
fi


# ClickHouse
CLICKHOUSE_COUNT=$(curl -s \
  "http://localhost:8123/?query=SELECT%20count()%20FROM%20atlas_dw.fact_transaction&user=default&password=$(grep '^CLICKHOUSE_PASSWORD=' .env | cut -d'=' -f2-)")

if [[ "$CLICKHOUSE_COUNT" =~ ^[0-9]+$ ]]
then
    echo "ClickHouse: OK ($CLICKHOUSE_COUNT rows)"
else
    echo "ClickHouse: FAILED"
    FAILED=1
fi

echo "========================================"

if [ "$FAILED" -eq 0 ]; then
    echo "Overall Status: HEALTHY"
    exit 0
else
    echo "Overall Status: UNHEALTHY"
    exit 1
fi
