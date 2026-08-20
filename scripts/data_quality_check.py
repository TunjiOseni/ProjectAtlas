import os
import requests

from utils.logger import get_logger

from dotenv import load_dotenv

logger = get_logger("data_quality")


load_dotenv("/home/tijay/Projects/ProjectAtlas/.env")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

CLICKHOUSE_URL = f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/"


def run_query(query):
    response = requests.post(
        CLICKHOUSE_URL,
        params={
            "query": query,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.text.strip()


def check_zero(name, query):
    count = int(run_query(query))
    logger.info("%s: %s", name, count)


    if count != 0:
        raise Exception(
            f"DATA QUALITY FAILED: {name} returned {count}"
        )


def main():

    logger.info("Starting ProjectAtlas data quality checks")

    print("========================================")
    print(" ProjectAtlas Data Quality Check")
    print("========================================")

    # 1. Duplicate customers
    check_zero(
        "Duplicate customer numbers",
        """
        SELECT count()
        FROM
        (
            SELECT customer_number
            FROM atlas_dw.dim_customer
            GROUP BY customer_number
            HAVING count() > 1
        )
        """
    )

    # 2. Duplicate accounts
    check_zero(
        "Duplicate account numbers",
        """
        SELECT count()
        FROM
        (
            SELECT account_number
            FROM atlas_dw.dim_account
            GROUP BY account_number
            HAVING count() > 1
        )
        """
    )

    # 3. Accounts without customers
    check_zero(
        "Accounts with invalid customer",
        """
        SELECT count()
        FROM atlas_dw.dim_account AS a
        LEFT JOIN atlas_dw.dim_customer AS c
            ON a.customer_id = c.customer_id
        WHERE c.customer_id = 0
        """
    )

    # 4. Transactions without accounts
    check_zero(
        "Transactions with invalid account",
        """
        SELECT count()
        FROM
        (
            SELECT *
            FROM atlas_dw.fact_transaction FINAL
        ) AS f
        LEFT JOIN atlas_dw.dim_account AS a
            ON f.account_id = a.account_id
        WHERE a.account_id = 0
        """
    )

    # 5. Transactions without customers
    check_zero(
        "Transactions with invalid customer",
        """
        SELECT count()
        FROM
        (
            SELECT *
            FROM atlas_dw.fact_transaction FINAL
        ) AS f
        LEFT JOIN atlas_dw.dim_customer AS c
            ON f.customer_id = c.customer_id
        WHERE f.customer_id IS NOT NULL
          AND c.customer_id = 0
        """
    )

    # 6. Missing transaction business keys
    check_zero(
        "Missing transaction business keys",
        """
        SELECT count()
        FROM atlas_dw.fact_transaction FINAL
        WHERE source_tran_id = ''
           OR part_tran_srl_num = 0
        """
    )

    # 7. Negative transaction amounts
    check_zero(
        "Negative transaction amounts",
        """
        SELECT count()
        FROM atlas_dw.fact_transaction FINAL
        WHERE transaction_amount < 0
        """
    )

    # 8. Invalid delete flags
    check_zero(
        "Invalid delete flags",
        """
        SELECT count()
        FROM atlas_dw.fact_transaction FINAL
        WHERE delete_flag IS NOT NULL
          AND delete_flag NOT IN ('Y', 'N')
        """
    )

    # 9. Invalid CDC operations
    check_zero(
        "Invalid CDC operations",
        """
        SELECT count()
        FROM atlas_dw.fact_transaction_cdc_history
        WHERE cdc_op NOT IN ('c', 'u', 'd', 'b')
        """
    )

    logger.info("All ProjectAtlas data quality checks passed")


if __name__ == "__main__":

    try:
        main()
    except Exception:
        logger.exception("ProjectAtlas data quality checks failed")
        raise
