import os
import json
import requests
from dotenv import load_dotenv

from etl.extract.extract_account import extract_accounts
from etl.transform.transform_account import transform_accounts

load_dotenv()

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "atlas_dw")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")


def load_accounts(accounts):
    url = f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/"

    # --------------------------------------------------
    # Find accounts already loaded
    # --------------------------------------------------
    response = requests.get(
        url,
        params={
            "query": f"""
                SELECT account_id
                FROM {CLICKHOUSE_DATABASE}.dim_account
                FORMAT JSON
            """,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        timeout=30,
    )

    response.raise_for_status()

    existing_ids = {
        row["account_id"]
        for row in response.json()["data"]
    }

    accounts_to_load = [
        account
        for account in accounts
        if account["account_id"] not in existing_ids
    ]

    if not accounts_to_load:
        print("No new accounts to load")
        return

    # --------------------------------------------------
    # Insert new accounts
    # --------------------------------------------------
    query = f"""
        INSERT INTO {CLICKHOUSE_DATABASE}.dim_account
        FORMAT JSONEachRow
    """

    rows = []

    for account in accounts_to_load:
        row = account.copy()

        row["account_open_date"] = (
            account["account_open_date"].strftime("%Y-%m-%d")
            if account["account_open_date"]
            else None
        )

        row["last_transaction_date"] = (
            account["last_transaction_date"].strftime("%Y-%m-%d")
            if account["last_transaction_date"]
            else None
        )

        row["created_date"] = (
            account["created_date"].strftime("%Y-%m-%d %H:%M:%S.%f")
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
        f"Loaded {len(accounts_to_load)} new accounts into ClickHouse"
    )


if __name__ == "__main__":
    accounts = extract_accounts()

    transformed_accounts = transform_accounts(accounts)

    load_accounts(transformed_accounts)
