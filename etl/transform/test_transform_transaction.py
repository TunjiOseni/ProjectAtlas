from etl.extract.extract_transaction import extract_transactions
from etl.transform.transform_transaction import transform_transactions

transactions = extract_transactions()

transformed_transactions = transform_transactions(transactions)

print(f"Transformed {len(transformed_transactions)} transactions")

for transaction in transformed_transactions:
    print(transaction)
