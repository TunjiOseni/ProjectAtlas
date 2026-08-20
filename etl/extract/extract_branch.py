import oracledb
import os
from dotenv import load_dotenv

load_dotenv("/home/tijay/Projects/ProjectAtlas/.env")


def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN"),
    )


def extract_branches():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            branch_id,
            branch_code,
            branch_name,
            branch_status
        FROM dim_branch
        ORDER BY branch_id
    """)

    columns = [col[0] for col in cursor.description]

    branches = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

    cursor.close()
    connection.close()

    return branches


if __name__ == "__main__":
    branches = extract_branches()

    print(f"Extracted {len(branches)} branches")

    for branch in branches:
        print(branch)
