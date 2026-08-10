import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

def get_connection():
    return oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN
    )


def extract_customers():
    query = """
        SELECT
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
        FROM dim_customer
        ORDER BY customer_id
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        customers = [
            dict(zip(columns, row))
            for row in rows
        ]

        return customers

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    customers = extract_customers()

    print(f"Extracted {len(customers)} customers")

    for customer in customers:
        print(customer)
