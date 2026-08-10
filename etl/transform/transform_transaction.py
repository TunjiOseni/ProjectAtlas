def transform_transactions(transactions):
    transformed = []

    for transaction in transactions:
        transformed_transaction = {
            "transaction_id": transaction["TRANSACTION_ID"],
            "date_id": transaction["DATE_ID"],
            "time_id": transaction["TIME_ID"],
            "value_date_id": transaction["VALUE_DATE_ID"],

            "account_id": transaction["ACCOUNT_ID"],
            "customer_id": transaction["CUSTOMER_ID"],
            "transaction_branch_id": transaction["TRANSACTION_BRANCH_ID"],
            "currency_id": transaction["CURRENCY_ID"],

            "tran_type_code": (
                transaction["TRAN_TYPE_CODE"].strip().upper()
                if transaction["TRAN_TYPE_CODE"]
                else None
            ),

            "tran_sub_type_code": (
                transaction["TRAN_SUB_TYPE_CODE"].strip().upper()
                if transaction["TRAN_SUB_TYPE_CODE"]
                else None
            ),

            "part_tran_type_code": (
                transaction["PART_TRAN_TYPE_CODE"].strip().upper()
                if transaction["PART_TRAN_TYPE_CODE"]
                else None
            ),

            "channel_code": (
                transaction["CHANNEL_CODE"].strip().upper()
                if transaction["CHANNEL_CODE"]
                else None
            ),

            "rate_id": transaction["RATE_ID"],

            "source_tran_id": transaction["SOURCE_TRAN_ID"].strip(),
            "part_tran_srl_num": transaction["PART_TRAN_SRL_NUM"],

            "gl_sub_head_code": transaction["GL_SUB_HEAD_CODE"],
            "module_id": transaction["MODULE_ID"],
            "bank_id": transaction["BANK_ID"],

            "transaction_amount": (
                float(transaction["TRANSACTION_AMOUNT"])
                if transaction["TRANSACTION_AMOUNT"] is not None
                else None
            ),

            "reference_amount": (
                float(transaction["REFERENCE_AMOUNT"])
                if transaction["REFERENCE_AMOUNT"] is not None
                else None
            ),

            "fx_transaction_amount": (
                float(transaction["FX_TRANSACTION_AMOUNT"])
                if transaction["FX_TRANSACTION_AMOUNT"] is not None
                else None
            ),

            "exchange_rate": (
                float(transaction["EXCHANGE_RATE"])
                if transaction["EXCHANGE_RATE"] is not None
                else None
            ),

            "reference_currency_code": transaction["REFERENCE_CURRENCY_CODE"],
            "reference_number": transaction["REFERENCE_NUMBER"],

            "transaction_particular": transaction["TRANSACTION_PARTICULAR"],
            "transaction_particular_2": transaction["TRANSACTION_PARTICULAR_2"],

            "entry_user_id": transaction["ENTRY_USER_ID"],
            "posted_user_id": transaction["POSTED_USER_ID"],
            "verified_user_id": transaction["VERIFIED_USER_ID"],

            "transaction_date": transaction["TRANSACTION_DATE"],
            "entry_date": transaction["ENTRY_DATE"],
            "posted_date": transaction["POSTED_DATE"],
            "verified_date": transaction["VERIFIED_DATE"],
            "gl_date": transaction["GL_DATE"],

            "transaction_status": (
                transaction["TRANSACTION_STATUS"].strip().upper()
                if transaction["TRANSACTION_STATUS"]
                else None
            ),

            "delete_flag": (
                transaction["DELETE_FLAG"].strip().upper()
                if transaction["DELETE_FLAG"]
                else None
            ),

            "created_date": transaction["CREATED_DATE"],
        }

        transformed.append(transformed_transaction)

    return transformed
