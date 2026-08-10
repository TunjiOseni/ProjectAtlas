from etl.extract.extract_customer import extract_customers
from etl.transform.transform_customer import transform_customers


customers = extract_customers()

transformed_customers = transform_customers(customers)

print(f"Transformed {len(transformed_customers)} customers")

for customer in transformed_customers:
    print(customer)
