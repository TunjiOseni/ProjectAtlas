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
        dsn=ORACLE_DSN,
    )


def extract_accounts():
    query = """
        SELECT
            account_id,
            source_acid,
            account_number,
            customer_id,
            schm_id,
            branch_id,
            currency_id,
            account_name,
            account_type,
            account_class,
            account_status,
            account_open_date,
            available_balance,
            ledger_balance,
            uncleared_balance,
            hold_amount,
            minimum_balance,
            overdraft_limit,
            cum_credit_amt,
            cum_debit_amt,
            last_transaction_date,
            created_date
        FROM dim_account
        ORDER BY account_id
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        accounts = [
            dict(zip(columns, row))
            for row in rows
        ]

        return accounts

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    accounts = extract_accounts()

    print(f"Extracted {len(accounts)} accounts")

    for account in accounts:
        print(account)
