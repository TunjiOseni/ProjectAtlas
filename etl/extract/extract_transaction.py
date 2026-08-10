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


def extract_transactions():
    query = """
        SELECT
            transaction_id,
            date_id,
            time_id,
            value_date_id,
            account_id,
            customer_id,
            transaction_branch_id,
            currency_id,
            tran_type_code,
            tran_sub_type_code,
            part_tran_type_code,
            channel_code,
            rate_id,
            source_tran_id,
            part_tran_srl_num,
            gl_sub_head_code,
            module_id,
            bank_id,
            transaction_amount,
            reference_amount,
            fx_transaction_amount,
            exchange_rate,
            reference_currency_code,
            reference_number,
            transaction_particular,
            transaction_particular_2,
            entry_user_id,
            posted_user_id,
            verified_user_id,
            transaction_date,
            entry_date,
            posted_date,
            verified_date,
            gl_date,
            transaction_status,
            delete_flag,
            created_date
        FROM fact_transaction
        ORDER BY transaction_id
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        transactions = [
            dict(zip(columns, row))
            for row in rows
        ]

        return transactions

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    transactions = extract_transactions()

    print(f"Extracted {len(transactions)} transactions")

    for transaction in transactions:
        print(transaction)
