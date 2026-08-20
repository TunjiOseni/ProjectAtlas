# ProjectAtlas

ProjectAtlas is an end-to-end banking data engineering project that combines batch ETL, real-time CDC streaming, data quality, orchestration, monitoring, and alerting.

## Architecture

Oracle
  ↓
Debezium
  ↓
Kafka
  ↓
Spark Structured Streaming
  ├── fact_transaction
  ├── fact_transaction_cdc_history
  └── fact_transaction_cdc_dlq

Batch ETL
  ↓
dim_branch
dim_customer
dim_account

Airflow
  ↓
ETL orchestration
Data quality checks
Success/failure email notifications

ClickHouse
  ↓
Grafana dashboards


## Technology Stack

- Oracle Database
- Python
- PySpark / Spark Structured Streaming
- Apache Kafka
- Debezium
- ClickHouse
- Apache Airflow
- Grafana
- Docker
- SQL


## Project Components

### Batch ETL

Python ETL jobs extract banking reference and dimensional data from Oracle, transform the data, and load it into ClickHouse.

Current dimension tables:

- `dim_branch`
- `dim_customer`
- `dim_account`

### Real-Time CDC

Oracle transaction changes are captured through Debezium and published to Kafka.

Spark Structured Streaming consumes the Kafka CDC events and writes them into ClickHouse.

### Current Transaction State

`fact_transaction`

Stores the latest logical state of each transaction using ClickHouse `ReplacingMergeTree` semantics.

### CDC History

`fact_transaction_cdc_history`

Append-only table that preserves the full lifecycle of transaction CDC events such as:

- Insert
- Update
- Delete

### Dead-Letter Queue

`fact_transaction_cdc_dlq`

Stores invalid CDC events that fail validation.

Validation includes checks for:

- Missing transaction ID
- Missing date ID
- Missing account ID
- Missing source transaction ID
- Invalid transaction serial number
- Missing event version
- Invalid CDC operation
- Missing created date

Invalid records are routed to the DLQ while valid records continue through the streaming pipeline.

## Data Quality

ProjectAtlas includes automated data-quality checks for:

- Duplicate customer numbers
- Duplicate account numbers
- Invalid customer relationships
- Invalid account relationships
- Missing transaction business keys
- Negative transaction amounts
- Invalid delete flags
- Invalid CDC operations

The data-quality checks are integrated into Airflow.

## Logging

ProjectAtlas uses centralized Python logging.

Main log file:

```text
logs/projectatlas.log
