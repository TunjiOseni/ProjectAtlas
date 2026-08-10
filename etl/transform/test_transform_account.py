from etl.extract.extract_account import extract_accounts
from etl.transform.transform_account import transform_accounts

accounts = extract_accounts()

transformed_accounts = transform_accounts(accounts)

print(f"Transformed {len(transformed_accounts)} accounts")

for account in transformed_accounts:
    print(account)
