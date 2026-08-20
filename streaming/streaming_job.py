from pyspark.sql import SparkSession

from streaming.kafka_reader import read_kafka_stream
from streaming.transformer import transform_transactions
from streaming.clickhouse_writer import write_to_clickhouse


CHECKPOINT_LOCATION = (
    "file:///home/tijay/Projects/ProjectAtlas/"
    "checkpoints/fact_transaction"
)


def main():

    spark = (
        SparkSession.builder
        .appName("ProjectAtlasTransactionStreaming")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    kafka_df = read_kafka_stream(spark)

    transaction_df = transform_transactions(kafka_df)

    query = (
        transaction_df.writeStream
        .foreachBatch(write_to_clickhouse)
        .option("checkpointLocation", CHECKPOINT_LOCATION)
        .trigger(processingTime="10 seconds")
        .start()
    )

    print(
        "ProjectAtlas is streaming Oracle transaction CDC "
        "from Kafka into ClickHouse."
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
