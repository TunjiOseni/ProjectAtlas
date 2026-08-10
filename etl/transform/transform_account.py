def transform_accounts(accounts):
    transformed = []

    for account in accounts:
        transformed_account = {
            "account_id": account["ACCOUNT_ID"],
            "source_acid": account["SOURCE_ACID"],
            "account_number": account["ACCOUNT_NUMBER"],
            "customer_id": account["CUSTOMER_ID"],
            "schm_id": account["SCHM_ID"],
            "branch_id": account["BRANCH_ID"],
            "currency_id": account["CURRENCY_ID"],
            "account_name": account["ACCOUNT_NAME"].strip(),
            "account_type": account["ACCOUNT_TYPE"].strip().upper(),
            "account_class": account["ACCOUNT_CLASS"].strip().upper(),
            "account_status": account["ACCOUNT_STATUS"].strip().upper(),
            "account_open_date": account["ACCOUNT_OPEN_DATE"],
            "available_balance": float(account["AVAILABLE_BALANCE"] or 0),
            "ledger_balance": float(account["LEDGER_BALANCE"] or 0),
            "uncleared_balance": float(account["UNCLEARED_BALANCE"] or 0),
            "hold_amount": float(account["HOLD_AMOUNT"] or 0),
            "minimum_balance": float(account["MINIMUM_BALANCE"] or 0),
            "overdraft_limit": float(account["OVERDRAFT_LIMIT"] or 0),
            "cum_credit_amt": float(account["CUM_CREDIT_AMT"] or 0),
            "cum_debit_amt": float(account["CUM_DEBIT_AMT"] or 0),
            "last_transaction_date": account["LAST_TRANSACTION_DATE"],
            "created_date": account["CREATED_DATE"],
        }

        transformed.append(transformed_account)

    return transformed
