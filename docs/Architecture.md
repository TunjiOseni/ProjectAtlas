# ProjectAtlas Architecture

## 1. Objective

ProjectAtlas is an enterprise-style banking data platform designed to demonstrate batch data engineering, real-time Change Data Capture (CDC), data warehousing, orchestration, data quality, monitoring, and alerting.

---

## 2. High-Level Architecture

The platform supports two primary data-processing paths:

### Batch Processing

Oracle Database
    |
    v
Python ETL
    |
    v
ClickHouse
    |
    v
Grafana

The batch pipeline loads dimensional and transactional data into the analytical warehouse.

### Real-Time CDC Processing

Oracle Database
    |
    v
Debezium
    |
    v
Apache Kafka
    |
    v
Spark Structured Streaming
    |
    +-------------------------------+
    |               |               |
    v               v               v
Current State    CDC History        DLQ
fact_transaction fact_transaction_  fact_transaction_
                 cdc_history        cdc_dlq
    |
    v
ClickHouse
    |
    v
Grafana

---

## 3. Source System

### Oracle Database

Oracle Database Free acts as the transactional source system.

The source contains banking entities such as:

- Customers
- Accounts
- Branches
- Transactions
- Transaction types
- Currencies
- Channels
- Rates

Oracle also acts as the source for transaction CDC events.

---

## 4. Batch ETL

Python-based ETL jobs extract data from Oracle, transform it, and load it into ClickHouse.

The main dimensional tables currently loaded into ClickHouse are:

- `dim_branch`
- `dim_customer`
- `dim_account`

The batch workflow is orchestrated by Apache Airflow.

---

## 5. Change Data Capture

Debezium captures changes to Oracle transaction data.

The CDC flow is:

Oracle
    |
    v
Debezium
    |
    v
Kafka topic:
atlas.BANKING.FACT_TRANSACTION

CDC operations include:

- `c` - Create
- `u` - Update
- `d` - Delete

---

## 6. Stream Processing

Apache Spark Structured Streaming consumes transaction CDC events from Kafka.

Spark performs:

- JSON parsing
- Debezium envelope processing
- CDC operation handling
- Data transformation
- Data validation
- Event version generation
- Soft-delete handling
- DLQ routing
- ClickHouse writes

Kafka offsets are used as CDC event versions.

---

## 7. Current-State Transaction Table

### `fact_transaction`

This table represents the current/latest state of transaction records.

Valid CDC events are written to this table after transformation and validation.

The transaction business key is based on:

- `source_tran_id`
- `part_tran_srl_num`

---

## 8. CDC History

### `fact_transaction_cdc_history`

This is an append-only history table.

It preserves valid CDC events so transaction changes can be audited over time.

Examples include:

- Original transaction creation
- Subsequent updates
- Delete events

---

## 9. Dead-Letter Queue

### `fact_transaction_cdc_dlq`

Invalid CDC events are routed to the DLQ instead of stopping the streaming pipeline.

Each rejected event can contain information such as:

- Source transaction ID
- CDC operation
- Event version
- Kafka timestamp
- Error reason
- Raw payload
- Creation timestamp

This allows valid events in the same micro-batch to continue processing.

---

## 10. Data Warehouse

ClickHouse is used as the analytical warehouse.

Current ProjectAtlas tables are:

- `dim_account`
- `dim_branch`
- `dim_customer`
- `fact_transaction`
- `fact_transaction_cdc_history`
- `fact_transaction_cdc_dlq`

---

## 11. Workflow Orchestration

Apache Airflow orchestrates the batch ETL and data-quality workflow.

The main execution flow is:

branch_etl
    |
    v
customer_etl
    |
    v
account_etl
    |
    v
transaction_etl
    |
    v
data_quality_check
    |
    v
advanced_data_quality_check
    |
    v
send_success_email

Failure callbacks provide failure notifications.

---

## 12. Data Quality

ProjectAtlas performs automated data-quality validation.

Checks include areas such as:

- Duplicate business keys
- Invalid relationships
- Missing transaction identifiers
- Invalid transaction amounts
- Invalid delete flags
- Invalid CDC operations

Streaming validation separates valid and invalid records so malformed events do not stop the pipeline.

---

## 13. Logging and Alerting

ProjectAtlas uses centralized application logging.

Primary log:

`logs/projectatlas.log`

Streaming runtime output is also captured in:

`logs/streaming.log`

Airflow provides success and failure email notifications.

---

## 14. Monitoring

Grafana provides dashboards for analytical and operational monitoring of ProjectAtlas data stored in ClickHouse.

---

## 15. Technology Stack

| Layer | Technology |
|---|---|
| Source Database | Oracle Database Free |
| CDC | Debezium |
| Messaging | Apache Kafka |
| Batch Processing | Python |
| Stream Processing | Apache Spark Structured Streaming |
| Data Warehouse | ClickHouse |
| Orchestration | Apache Airflow |
| Monitoring | Grafana |
| Containerization | Docker / Docker Compose |
| Development Environment | Ubuntu on WSL2 |
| Primary Language | Python |

---

## 16. End-to-End Flow

ProjectAtlas demonstrates the following end-to-end data engineering capabilities:

Oracle
    |
    +---- Batch ETL ----> ClickHouse
    |
    +---- Debezium
             |
             v
           Kafka
             |
             v
      Spark Structured Streaming
             |
       +-----+-----+
       |     |     |
       v     v     v
     Current History DLQ
       |
       v
    ClickHouse
       |
       v
     Grafana

Airflow provides orchestration, data-quality execution, and email notifications around the batch workflow.
