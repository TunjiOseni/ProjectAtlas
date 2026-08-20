import os
import json
import requests
from dotenv import load_dotenv
from utils.logger import get_logger

from etl.extract.extract_branch import extract_branches
from etl.transform.transform_branch import transform_branches

load_dotenv("/home/tijay/Projects/ProjectAtlas/.env")

logger = get_logger("load_branch")

CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "http://localhost:8123")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")


def load_branches(branches):

    if not branches:
        print("No branches to load.")
        return

    # -----------------------------------------
    # STEP 1: Clear the existing branch records
    # -----------------------------------------

    truncate_query = "TRUNCATE TABLE atlas_dw.dim_branch"

    response = requests.post(
        CLICKHOUSE_URL,
        params={
            "query": truncate_query,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
    )

    response.raise_for_status()


    logger.info("Existing dim_branch data cleared")


    # -----------------------------------------
    # STEP 2: Prepare the new branch records
    # -----------------------------------------

    values = []

    for branch in branches:
        values.append(
            (
                branch["branch_id"],
                branch["branch_code"],
                branch["branch_name"],
                branch["branch_status"],
            )
        )

    query = """
        INSERT INTO atlas_dw.dim_branch
        (
            branch_id,
            branch_code,
            branch_name,
            branch_status
        )
        FORMAT JSONEachRow
    """

    rows = "\n".join(
        json.dumps({
            "branch_id": row[0],
            "branch_code": row[1],
            "branch_name": row[2],
            "branch_status": row[3],
        })
        for row in values
    )


    # -----------------------------------------
    # STEP 3: Load the current Oracle data
    # -----------------------------------------

    response = requests.post(
        CLICKHOUSE_URL,
        params={
            "query": query,
            "user": CLICKHOUSE_USER,
            "password": CLICKHOUSE_PASSWORD,
        },
        data=rows,
    )

    response.raise_for_status()


    logger.info(
    "Loaded %s branches into ClickHouse",
    len(branches)
)


if __name__ == "__main__":

    try:
        logger.info("Starting branch ETL")

        branches = extract_branches()

        logger.info(
            "Extracted %s branches from Oracle",
            len(branches)
        )

        branches = transform_branches(branches)

        logger.info(
            "Transformed %s branches",
            len(branches)
        )

        load_branches(branches)

        logger.info("Branch ETL completed successfully")

    except Exception:
        logger.exception("Branch ETL failed")
        raise
