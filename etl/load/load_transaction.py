import os
import json
import requests
from dotenv import load_dotenv

from etl.extract.extract_transaction import extract_transactions
from etl.transform.transform_transaction import transform_transactions

load_dotenv()

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "atlas_dw")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")


def format_date(value):
    if value is None:
        return None

    return value.strftime("%Y-%m-%d")


def format_datetime(value):
    if value is None:
        return None

    return value.strftime("%Y-%m-%d %H:%M:%S.%f")


def load_transactions(transactions):
    url = f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/"

    # ---------------------------------------------------------
    # Read transactions already loaded
    #
    # Business grain:
    # source_tran_id + part_tran_srl_num
    # ---------------------------------------------------------
    response = requests.get(
        url,
        params={
            "query": f"""
                SELECT
                    source_tran_id,
                    part_tran_srl_num
                FROM {CLICKHOUSE_DATABASE}.fact_transaction
                FORMAT JSON
            """,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        timeout=30,
    )

    response.raise_for_status()

    existing_transactions = {
        (
            row["source_tran_id"],
            row["part_tran_srl_num"],
        )
        for row in response.json()["data"]
    }

    # ---------------------------------------------------------
    # Remove transactions already loaded
    # ---------------------------------------------------------
    transactions_to_load = [
        transaction
        for transaction in transactions
        if (
            transaction["source_tran_id"],
            transaction["part_tran_srl_num"],
        )
        not in existing_transactions
    ]

    if not transactions_to_load:
        print("No new transactions to load")
        return

    # ---------------------------------------------------------
    # Insert into ClickHouse
    # ---------------------------------------------------------
    query = f"""
        INSERT INTO {CLICKHOUSE_DATABASE}.fact_transaction
        FORMAT JSONEachRow
    """

    rows = []

    for transaction in transactions_to_load:
        row = transaction.copy()

        row["transaction_date"] = format_date(
            transaction["transaction_date"]
        )

        row["entry_date"] = format_date(
            transaction["entry_date"]
        )

        row["posted_date"] = format_date(
            transaction["posted_date"]
        )

        row["verified_date"] = format_date(
            transaction["verified_date"]
        )

        row["gl_date"] = format_date(
            transaction["gl_date"]
        )

        row["created_date"] = format_datetime(
            transaction["created_date"]
        )

        rows.append(row)

    payload = "\n".join(
        json.dumps(row)
        for row in rows
    )

    response = requests.post(
        url,
        params={
            "query": query,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        data=payload,
        timeout=30,
    )

    response.raise_for_status()

    print(
        f"Loaded {len(transactions_to_load)} "
        "new transactions into ClickHouse"
    )


if __name__ == "__main__":
    transactions = extract_transactions()

    transformed_transactions = transform_transactions(
        transactions
    )

    load_transactions(transformed_transactions)
