import os
import json
import requests
from dotenv import load_dotenv
from utils.logger import get_logger


from etl.extract.extract_customer import extract_customers
from etl.transform.transform_customer import transform_customers

load_dotenv()

logger = get_logger("load_customer")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "atlas_dw")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")


def load_customers(customers):
    url = f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/"

    # ---------------------------------------------------------
    # Get customer IDs already loaded into ClickHouse
    # ---------------------------------------------------------
    existing_response = requests.get(
        url,
        params={
            "query": f"""
                SELECT customer_id
                FROM {CLICKHOUSE_DATABASE}.dim_customer
                FORMAT JSON
            """,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        timeout=30,
    )

    existing_response.raise_for_status()

    existing_data = existing_response.json()

    existing_ids = {
        row["customer_id"]
        for row in existing_data["data"]
    }

    # ---------------------------------------------------------
    # Only load customers that do not already exist
    # ---------------------------------------------------------
    customers_to_load = [
        customer
        for customer in customers
        if customer["customer_id"] not in existing_ids
    ]

    if not customers_to_load:
        print("No new customers to load")
        return

    # ---------------------------------------------------------
    # ClickHouse INSERT
    # ---------------------------------------------------------
    query = f"""
        INSERT INTO {CLICKHOUSE_DATABASE}.dim_customer
        (
            customer_id,
            source_customer_id,
            customer_number,
            customer_type,
            customer_segment,
            full_name,
            mobile_number,
            email_address,
            home_branch_id,
            preferred_currency_id,
            customer_status,
            created_date
        )
        FORMAT JSONEachRow
    """

    rows = []

    for customer in customers_to_load:
        row = {
            "customer_id": customer["customer_id"],
            "source_customer_id": customer["source_customer_id"],
            "customer_number": customer["customer_number"],
            "customer_type": customer["customer_type"],
            "customer_segment": customer["customer_segment"],
            "full_name": customer["full_name"],
            "mobile_number": customer["mobile_number"],
            "email_address": customer["email_address"],
            "home_branch_id": customer["home_branch_id"],
            "preferred_currency_id": customer["preferred_currency_id"],
            "customer_status": customer["customer_status"],
            "created_date": customer["created_date"].strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            ),
        }

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

    logger.info(
    "Loaded %s customers into ClickHouse",
    len(customers)
)


if __name__ == "__main__":

    if __name__ == "__main__":

        try:
            logger.info("Starting customer ETL")

            customers = extract_customers()

            logger.info(
            "Extracted %s customers from Oracle",
            len(customers)
        )

            customers = transform_customers(customers)
            
            logger.info(
            "Transformed %s customers",
            len(customers)
        )

            load_customers(customers)

            logger.info("Customer ETL completed successfully")

        except Exception:

                logger.exception("Customer ETL failed")

                raise
