from etl.extract.extract_customer import extract_customers
from etl.transform.transform_customer import transform_customers
from etl.load.load_customer import load_customers

from etl.extract.extract_account import extract_accounts
from etl.transform.transform_account import transform_accounts
from etl.load.load_account import load_accounts

from etl.extract.extract_transaction import extract_transactions
from etl.transform.transform_transaction import transform_transactions
from etl.load.load_transaction import load_transactions


def run_customer_etl():
    print("\n=== CUSTOMER ETL ===")

    customers = extract_customers()
    print(f"Extracted {len(customers)} customers")

    customers = transform_customers(customers)
    print(f"Transformed {len(customers)} customers")

    load_customers(customers)


def run_account_etl():
    print("\n=== ACCOUNT ETL ===")

    accounts = extract_accounts()
    print(f"Extracted {len(accounts)} accounts")

    accounts = transform_accounts(accounts)
    print(f"Transformed {len(accounts)} accounts")

    load_accounts(accounts)


def run_transaction_etl():
    print("\n=== TRANSACTION ETL ===")

    transactions = extract_transactions()
    print(f"Extracted {len(transactions)} transactions")

    transactions = transform_transactions(transactions)
    print(f"Transformed {len(transactions)} transactions")

    load_transactions(transactions)


def main():
    print("================================")
    print("PROJECT ATLAS ETL STARTED")
    print("================================")

    run_customer_etl()
    run_account_etl()
    run_transaction_etl()

    print("\n================================")
    print("PROJECT ATLAS ETL COMPLETED")
    print("================================")


if __name__ == "__main__":
    main()
