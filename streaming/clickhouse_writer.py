import os

from dotenv import load_dotenv
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from utils.logger import get_logger


load_dotenv("/home/tijay/Projects/ProjectAtlas/.env")

logger = get_logger("streaming")


CLICKHOUSE_URL = "jdbc:clickhouse:http://127.0.0.1:8123/atlas_dw"

CURRENT_TABLE = "fact_transaction"
HISTORY_TABLE = "fact_transaction_cdc_history"
DLQ_TABLE = "fact_transaction_cdc_dlq"

CLICKHOUSE_PROPERTIES = {
    "user": os.getenv("CLICKHOUSE_USER", "default"),
    "password": os.getenv("CLICKHOUSE_PASSWORD", ""),
    "driver": "com.clickhouse.jdbc.ClickHouseDriver",
}


def write_to_clickhouse(batch_df, batch_id):

    try:

        # -------------------------------------------------
        # Empty batch
        # -------------------------------------------------

        if batch_df.isEmpty():
            logger.info(
                "Batch %s: no records",
                batch_id
            )
            return


        # -------------------------------------------------
        # Record count
        # -------------------------------------------------

        batch_count = batch_df.count()

        logger.info(
            "Batch %s: received %s CDC records",
            batch_id,
            batch_count
        )


        # -------------------------------------------------
        # Build common transformed output
        # -------------------------------------------------

        output_df = batch_df.select(

            F.col("TRANSACTION_ID").alias("transaction_id"),
            F.col("DATE_ID").alias("date_id"),
            F.col("TIME_ID").alias("time_id"),
            F.col("VALUE_DATE_ID").alias("value_date_id"),

            F.col("ACCOUNT_ID").alias("account_id"),
            F.col("CUSTOMER_ID").alias("customer_id"),
            F.col("TRANSACTION_BRANCH_ID").alias(
                "transaction_branch_id"
            ),
            F.col("CURRENCY_ID").alias("currency_id"),

            F.col("TRAN_TYPE_CODE").alias("tran_type_code"),
            F.col("TRAN_SUB_TYPE_CODE").alias(
                "tran_sub_type_code"
            ),
            F.col("PART_TRAN_TYPE_CODE").alias(
                "part_tran_type_code"
            ),
            F.col("CHANNEL_CODE").alias("channel_code"),
            F.col("RATE_ID").alias("rate_id"),

            F.col("SOURCE_TRAN_ID").alias("source_tran_id"),
            F.col("PART_TRAN_SRL_NUM").alias(
                "part_tran_srl_num"
            ),

            F.col("GL_SUB_HEAD_CODE").alias(
                "gl_sub_head_code"
            ),
            F.col("MODULE_ID").alias("module_id"),
            F.col("BANK_ID").alias("bank_id"),

            F.col("TRANSACTION_AMOUNT").alias(
                "transaction_amount"
            ),
            F.col("REFERENCE_AMOUNT").alias(
                "reference_amount"
            ),
            F.col("FX_TRANSACTION_AMOUNT").alias(
                "fx_transaction_amount"
            ),
            F.col("EXCHANGE_RATE").alias("exchange_rate"),

            F.col("REFERENCE_CURRENCY_CODE").alias(
                "reference_currency_code"
            ),
            F.col("REFERENCE_NUMBER").alias(
                "reference_number"
            ),

            F.col("TRANSACTION_PARTICULAR").alias(
                "transaction_particular"
            ),
            F.col("TRANSACTION_PARTICULAR_2").alias(
                "transaction_particular_2"
            ),

            F.col("ENTRY_USER_ID").alias("entry_user_id"),
            F.col("POSTED_USER_ID").alias("posted_user_id"),
            F.col("VERIFIED_USER_ID").alias(
                "verified_user_id"
            ),

            F.col("TRANSACTION_DATE").alias(
                "transaction_date"
            ),
            F.col("ENTRY_DATE").alias("entry_date"),
            F.col("POSTED_DATE").alias("posted_date"),
            F.col("VERIFIED_DATE").alias("verified_date"),
            F.col("GL_DATE").alias("gl_date"),

            F.col("TRANSACTION_STATUS").alias(
                "transaction_status"
            ),
            F.col("DELETE_FLAG").alias("delete_flag"),

            F.col("CREATED_DATE").alias("created_date"),

            F.col("event_version").alias("event_version"),
            F.col("cdc_op").alias("cdc_op"),

            F.col("kafka_timestamp").alias(
                "kafka_timestamp"
            ),
        )


        # =================================================
        # VALIDATION / DLQ ROUTING
        # =================================================

        invalid_condition = (
            F.col("transaction_id").isNull()
            | F.col("date_id").isNull()
            | F.col("account_id").isNull()
            | F.col("source_tran_id").isNull()
            | (F.trim(F.col("source_tran_id")) == "")
            | F.col("part_tran_srl_num").isNull()
            | (F.col("part_tran_srl_num") == 0)
            | F.col("event_version").isNull()
            | F.col("cdc_op").isNull()
            | (~F.col("cdc_op").isin("b", "c", "u", "d"))
            | F.col("created_date").isNull()
        )


        # -------------------------------------------------
        # Invalid records
        # -------------------------------------------------

        invalid_df = output_df.filter(invalid_condition)


        dlq_df = (
            invalid_df
            .withColumn(
                "error_reason",
                F.concat_ws(
                    "; ",
                    F.when(
                        F.col("transaction_id").isNull(),
                        F.lit("Missing transaction_id")
                    ),
                    F.when(
                        F.col("date_id").isNull(),
                        F.lit("Missing date_id")
                    ),
                    F.when(
                        F.col("account_id").isNull(),
                        F.lit("Missing account_id")
                    ),
                    F.when(
                        F.col("source_tran_id").isNull()
                        | (F.trim(F.col("source_tran_id")) == ""),
                        F.lit("Missing source_tran_id")
                    ),
                    F.when(
                        F.col("part_tran_srl_num").isNull()
                        | (F.col("part_tran_srl_num") == 0),
                        F.lit("Invalid part_tran_srl_num")
                    ),
                    F.when(
                        F.col("event_version").isNull(),
                        F.lit("Missing event_version")
                    ),
                    F.when(
                        F.col("cdc_op").isNull()
                        | (~F.col("cdc_op").isin("b", "c", "u", "d")),
                        F.lit("Invalid cdc_op")
                    ),
                    F.when(
                        F.col("created_date").isNull(),
                        F.lit("Missing created_date")
                    ),
                )
            )
            .withColumn(
                "raw_payload",
                F.to_json(
                    F.struct(
                        *[
                            F.col(column)
                            for column in output_df.columns
                        ]
                    )
                )
            )
            .select(
                "source_tran_id",
                "cdc_op",
                "event_version",
                "kafka_timestamp",
                "error_reason",
                "raw_payload",
            )
        )


        invalid_count = dlq_df.count()

        if invalid_count > 0:

            logger.warning(
                "Batch %s: routing %s invalid records to DLQ",
                batch_id,
                invalid_count
            )

            (
                dlq_df.write
                .mode("append")
                .jdbc(
                    url=CLICKHOUSE_URL,
                    table=DLQ_TABLE,
                    properties=CLICKHOUSE_PROPERTIES,
                )
            )

            logger.warning(
                "Batch %s: DLQ write completed",
                batch_id
            )


        # -------------------------------------------------
        # Valid records
        # -------------------------------------------------

        valid_df = output_df.filter(~invalid_condition)

        valid_count = valid_df.count()

        logger.info(
            "Batch %s: %s valid records, %s invalid records",
            batch_id,
            valid_count,
            invalid_count
        )


        if valid_count == 0:

            logger.warning(
                "Batch %s: no valid records to process",
                batch_id
            )

            return


        # =================================================
        # 1. CDC HISTORY
        # =================================================

        history_df = valid_df.select(

            "transaction_id",
            "date_id",
            "time_id",
            "value_date_id",

            "account_id",
            "customer_id",
            "transaction_branch_id",
            "currency_id",

            "tran_type_code",
            "tran_sub_type_code",
            "part_tran_type_code",
            "channel_code",
            "rate_id",

            "source_tran_id",
            "part_tran_srl_num",

            "gl_sub_head_code",
            "module_id",
            "bank_id",

            "transaction_amount",
            "reference_amount",
            "fx_transaction_amount",
            "exchange_rate",

            "reference_currency_code",
            "reference_number",

            "transaction_particular",
            "transaction_particular_2",

            "entry_user_id",
            "posted_user_id",
            "verified_user_id",

            "transaction_date",
            "entry_date",
            "posted_date",
            "verified_date",
            "gl_date",

            "transaction_status",
            "delete_flag",

            "created_date",

            "cdc_op",
            "event_version",
            "kafka_timestamp",
        )


        history_count = history_df.count()

        logger.info(
            "Batch %s: writing %s records to CDC history",
            batch_id,
            history_count
        )


        (
            history_df.write
            .mode("append")
            .jdbc(
                url=CLICKHOUSE_URL,
                table=HISTORY_TABLE,
                properties=CLICKHOUSE_PROPERTIES,
            )
        )


        logger.info(
            "Batch %s: CDC history write completed",
            batch_id
        )


        # =================================================
        # 2. CURRENT STATE
        # =================================================

        window_spec = (
            Window
            .partitionBy(
                "source_tran_id",
                "part_tran_srl_num"
            )
            .orderBy(
                F.col("event_version").desc()
            )
        )


        current_df = (
            valid_df
            .withColumn(
                "row_num",
                F.row_number().over(window_spec)
            )
            .filter(
                F.col("row_num") == 1
            )
            .drop(
                "row_num",
                "kafka_timestamp"
            )
        )


        current_count = current_df.count()

        logger.info(
            "Batch %s: writing %s latest-state records",
            batch_id,
            current_count
        )


        (
            current_df.write
            .mode("append")
            .jdbc(
                url=CLICKHOUSE_URL,
                table=CURRENT_TABLE,
                properties=CLICKHOUSE_PROPERTIES,
            )
        )


        logger.info(
            "Batch %s: current-state write completed",
            batch_id
        )


    except Exception:

        logger.exception(
            "Batch %s: streaming write failed",
            batch_id
        )

        raise
