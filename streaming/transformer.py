from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    LongType
)


transaction_schema = StructType([
    StructField("TRANSACTION_ID", DoubleType()),
    StructField("DATE_ID", DoubleType()),
    StructField("TIME_ID", DoubleType()),
    StructField("VALUE_DATE_ID", DoubleType()),
    StructField("ACCOUNT_ID", DoubleType()),
    StructField("CUSTOMER_ID", DoubleType()),
    StructField("TRANSACTION_BRANCH_ID", DoubleType()),
    StructField("CURRENCY_ID", DoubleType()),

    StructField("TRAN_TYPE_CODE", StringType()),
    StructField("TRAN_SUB_TYPE_CODE", StringType()),
    StructField("PART_TRAN_TYPE_CODE", StringType()),
    StructField("CHANNEL_CODE", StringType()),

    StructField("RATE_ID", DoubleType()),
    StructField("SOURCE_TRAN_ID", StringType()),
    StructField("PART_TRAN_SRL_NUM", DoubleType()),

    StructField("GL_SUB_HEAD_CODE", StringType()),
    StructField("MODULE_ID", StringType()),
    StructField("BANK_ID", StringType()),

    StructField("TRANSACTION_AMOUNT", DoubleType()),
    StructField("REFERENCE_AMOUNT", DoubleType()),
    StructField("FX_TRANSACTION_AMOUNT", DoubleType()),
    StructField("EXCHANGE_RATE", DoubleType()),

    StructField("REFERENCE_CURRENCY_CODE", StringType()),
    StructField("REFERENCE_NUMBER", StringType()),
    StructField("TRANSACTION_PARTICULAR", StringType()),
    StructField("TRANSACTION_PARTICULAR_2", StringType()),

    StructField("ENTRY_USER_ID", StringType()),
    StructField("POSTED_USER_ID", StringType()),
    StructField("VERIFIED_USER_ID", StringType()),

    StructField("TRANSACTION_DATE", LongType()),
    StructField("ENTRY_DATE", LongType()),
    StructField("POSTED_DATE", LongType()),
    StructField("VERIFIED_DATE", LongType()),
    StructField("GL_DATE", LongType()),

    StructField("TRANSACTION_STATUS", StringType()),
    StructField("DELETE_FLAG", StringType()),

    StructField("CREATED_DATE", LongType())
])


payload_schema = StructType([
    StructField("before", transaction_schema),
    StructField("after", transaction_schema),
    StructField("op", StringType())
])


def transform_transactions(kafka_df):

    parsed_df = (
        kafka_df
        .select(
            F.from_json(
                F.col("value").cast("string"),
                StructType([
                    StructField(
                        "payload",
                        payload_schema
                    )
                ])
            ).alias("data"),
            F.col("topic"),
            F.col("partition"),
            F.col("offset"),
            F.col("timestamp").alias("kafka_timestamp")
        )
    )

    transaction_df = (
    parsed_df
    .select(
        "data.payload.*",
        "topic",
        "partition",
        "offset",
        "kafka_timestamp"
    )

    # Accept create, update and delete events
    .filter(F.col("op").isin("c", "u", "d"))

    # For DELETE, after is NULL, so use before.
    # For INSERT/UPDATE, use after.
    .withColumn(
        "record",
        F.when(
            F.col("op") == "d",
            F.col("before")
        ).otherwise(
            F.col("after")
        )
    )

    .select(
        "record.*",
        "op",
        "topic",
        "partition",
        "offset",
        "kafka_timestamp"
    )

    # Soft-delete marker
    .withColumn(
        "DELETE_FLAG",
        F.when(
            F.col("op") == "d",
            F.lit("Y")
        ).otherwise(
            F.coalesce(F.col("DELETE_FLAG"), F.lit("N"))
        )
    )

    # CDC version used by ClickHouse ReplacingMergeTree
    .withColumn(
        "event_version",
        F.col("offset").cast("long")
    )

    # Debezium operation: c, u or d
    .withColumn(
        "cdc_op",
        F.col("op")
    )
)

    return (
        transaction_df

        # Oracle NUMBER -> appropriate warehouse types
        .withColumn(
            "TRANSACTION_ID",
            F.col("TRANSACTION_ID").cast("long")
        )
        .withColumn(
            "DATE_ID",
            F.col("DATE_ID").cast("int")
        )
        .withColumn(
            "TIME_ID",
            F.col("TIME_ID").cast("int")
        )
        .withColumn(
            "VALUE_DATE_ID",
            F.col("VALUE_DATE_ID").cast("int")
        )
        .withColumn(
            "ACCOUNT_ID",
            F.col("ACCOUNT_ID").cast("long")
        )
        .withColumn(
            "CUSTOMER_ID",
            F.col("CUSTOMER_ID").cast("long")
        )
        .withColumn(
            "TRANSACTION_BRANCH_ID",
            F.col("TRANSACTION_BRANCH_ID").cast("long")
        )
        .withColumn(
            "CURRENCY_ID",
            F.col("CURRENCY_ID").cast("long")
        )
        .withColumn(
            "RATE_ID",
            F.col("RATE_ID").cast("long")
        )
        .withColumn(
            "PART_TRAN_SRL_NUM",
            F.col("PART_TRAN_SRL_NUM").cast("int")
        )

        # Monetary values
        .withColumn(
            "TRANSACTION_AMOUNT",
            F.col("TRANSACTION_AMOUNT").cast("decimal(18,2)")
        )
        .withColumn(
            "REFERENCE_AMOUNT",
            F.col("REFERENCE_AMOUNT").cast("decimal(18,2)")
        )
        .withColumn(
            "FX_TRANSACTION_AMOUNT",
            F.col("FX_TRANSACTION_AMOUNT").cast("decimal(18,2)")
        )
        .withColumn(
            "EXCHANGE_RATE",
            F.col("EXCHANGE_RATE").cast("decimal(20,8)")
        )

        # Debezium Timestamp = milliseconds since epoch
        .withColumn(
            "TRANSACTION_DATE",
            F.to_date(
                (F.col("TRANSACTION_DATE") / 1000)
            .cast("timestamp")
            )
        )
        .withColumn(
            "ENTRY_DATE",
            F.to_date(
                (F.col("ENTRY_DATE") / 1000)
            .cast("timestamp")
            )
        )
        .withColumn(
            "POSTED_DATE",
            F.to_date(
                (F.col("POSTED_DATE") / 1000)
            .cast("timestamp")
            )
        )
        .withColumn(
            "VERIFIED_DATE",
            F.to_date(
                (F.col("VERIFIED_DATE") / 1000)
            .cast("timestamp")
            )
        )
        .withColumn(
            "GL_DATE",
            F.to_date(
                (F.col("GL_DATE") / 1000)
            .cast("timestamp")
            )
        )

        # Debezium MicroTimestamp = microseconds since epoch
        .withColumn(
            "CREATED_DATE",
            (F.col("CREATED_DATE") / 1000000)
            .cast("timestamp")
        )
    )
