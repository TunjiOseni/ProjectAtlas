def transform_customers(customers):
    transformed = []

    for customer in customers:
        transformed_customer = {
            "customer_id": customer["CUSTOMER_ID"],
            "source_customer_id": customer["SOURCE_CUSTOMER_ID"],
            "customer_number": customer["CUSTOMER_NUMBER"],
            "customer_type": customer["CUSTOMER_TYPE"].strip().upper(),
            "customer_segment": customer["CUSTOMER_SEGMENT"].strip().upper(),
            "full_name": customer["FULL_NAME"].strip(),
            "mobile_number": (
                customer["MOBILE_NUMBER"].strip()
                if customer["MOBILE_NUMBER"]
                else None
            ),
            "email_address": (
                customer["EMAIL_ADDRESS"].strip().lower()
                if customer["EMAIL_ADDRESS"]
                else None
            ),
            "home_branch_id": customer["HOME_BRANCH_ID"],
            "preferred_currency_id": customer["PREFERRED_CURRENCY_ID"],
            "customer_status": customer["CUSTOMER_STATUS"].strip().upper(),
            "created_date": customer["CREATED_DATE"],
        }

        transformed.append(transformed_customer)

    return transformed
