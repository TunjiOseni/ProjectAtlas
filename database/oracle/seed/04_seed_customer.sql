/* =========================================================
   PROJECT ATLAS
   DIM_CUSTOMER SEED DATA
   ========================================================= */

/* Customer 1 */
MERGE INTO dim_customer d
USING (
    SELECT
        'CUST000001' AS customer_number,
        'SRC_CUST_000001' AS source_customer_id,
        'INDIVIDUAL' AS customer_type,
        'RETAIL' AS customer_segment,
        'Adebayo' AS first_name,
        'Oluwaseun' AS middle_name,
        'Johnson' AS last_name,
        'Adebayo Oluwaseun Johnson' AS full_name,
        DATE '1985-04-12' AS date_of_birth,
        'M' AS gender,
        '08031234567' AS mobile_number,
        'adebayo.johnson@example.com' AS email_address,
        'Calabar' AS city,
        'Cross River' AS state,
        'Nigeria' AS country,
        3 AS kyc_level,
        'LOW' AS risk_rating,
        15 AS customer_risk_score,
        'N' AS pep_flag,
        'N' AS blacklisted_flag,
        1 AS home_branch_id,
        1 AS preferred_currency_id,
        DATE '2019-06-15' AS customer_since
    FROM dual
) s
ON (d.customer_number = s.customer_number)

WHEN NOT MATCHED THEN
INSERT
(
    customer_number,
    source_customer_id,
    customer_type,
    customer_segment,
    first_name,
    middle_name,
    last_name,
    full_name,
    date_of_birth,
    gender,
    mobile_number,
    email_address,
    city,
    state,
    country,
    kyc_level,
    risk_rating,
    customer_risk_score,
    pep_flag,
    blacklisted_flag,
    home_branch_id,
    preferred_currency_id,
    customer_since
)
VALUES
(
    s.customer_number,
    s.source_customer_id,
    s.customer_type,
    s.customer_segment,
    s.first_name,
    s.middle_name,
    s.last_name,
    s.full_name,
    s.date_of_birth,
    s.gender,
    s.mobile_number,
    s.email_address,
    s.city,
    s.state,
    s.country,
    s.kyc_level,
    s.risk_rating,
    s.customer_risk_score,
    s.pep_flag,
    s.blacklisted_flag,
    s.home_branch_id,
    s.preferred_currency_id,
    s.customer_since
);


/* Customer 2 */
MERGE INTO dim_customer d
USING (
    SELECT
        'CUST000002' AS customer_number,
        'SRC_CUST_000002' AS source_customer_id,
        'INDIVIDUAL' AS customer_type,
        'RETAIL' AS customer_segment,
        'Chidinma' AS first_name,
        'Okafor' AS last_name,
        'Chidinma Okafor' AS full_name,
        DATE '1990-09-23' AS date_of_birth,
        'F' AS gender,
        '08062345678' AS mobile_number,
        'chidinma.okafor@example.com' AS email_address,
        'Enugu' AS city,
        'Enugu' AS state,
        'Nigeria' AS country,
        3 AS kyc_level,
        'LOW' AS risk_rating,
        10 AS customer_risk_score,
        'N' AS pep_flag,
        'N' AS blacklisted_flag,
        2 AS home_branch_id,
        1 AS preferred_currency_id,
        DATE '2020-02-10' AS customer_since
    FROM dual
) s
ON (d.customer_number = s.customer_number)

WHEN NOT MATCHED THEN
INSERT
(
    customer_number,
    source_customer_id,
    customer_type,
    customer_segment,
    first_name,
    last_name,
    full_name,
    date_of_birth,
    gender,
    mobile_number,
    email_address,
    city,
    state,
    country,
    kyc_level,
    risk_rating,
    customer_risk_score,
    pep_flag,
    blacklisted_flag,
    home_branch_id,
    preferred_currency_id,
    customer_since
)
VALUES
(
    s.customer_number,
    s.source_customer_id,
    s.customer_type,
    s.customer_segment,
    s.first_name,
    s.last_name,
    s.full_name,
    s.date_of_birth,
    s.gender,
    s.mobile_number,
    s.email_address,
    s.city,
    s.state,
    s.country,
    s.kyc_level,
    s.risk_rating,
    s.customer_risk_score,
    s.pep_flag,
    s.blacklisted_flag,
    s.home_branch_id,
    s.preferred_currency_id,
    s.customer_since
);


/* Customer 3 - SME */
MERGE INTO dim_customer d
USING (
    SELECT
        'CUST000003' AS customer_number,
        'SRC_CUST_000003' AS source_customer_id,
        'CORPORATE' AS customer_type,
        'SME' AS customer_segment,
        'Atlas Foods Limited' AS full_name,
        'Atlas Foods Limited' AS company_name,
        '08123456789' AS mobile_number,
        'accounts@atlasfoods.example.com' AS email_address,
        'Calabar' AS city,
        'Cross River' AS state,
        'Nigeria' AS country,
        3 AS kyc_level,
        'MEDIUM' AS risk_rating,
        35 AS customer_risk_score,
        'N' AS pep_flag,
        'N' AS blacklisted_flag,
        1 AS home_branch_id,
        1 AS preferred_currency_id,
        DATE '2018-11-01' AS customer_since
    FROM dual
) s
ON (d.customer_number = s.customer_number)

WHEN NOT MATCHED THEN
INSERT
(
    customer_number,
    source_customer_id,
    customer_type,
    customer_segment,
    full_name,
    company_name,
    mobile_number,
    email_address,
    city,
    state,
    country,
    kyc_level,
    risk_rating,
    customer_risk_score,
    pep_flag,
    blacklisted_flag,
    home_branch_id,
    preferred_currency_id,
    customer_since
)
VALUES
(
    s.customer_number,
    s.source_customer_id,
    s.customer_type,
    s.customer_segment,
    s.full_name,
    s.company_name,
    s.mobile_number,
    s.email_address,
    s.city,
    s.state,
    s.country,
    s.kyc_level,
    s.risk_rating,
    s.customer_risk_score,
    s.pep_flag,
    s.blacklisted_flag,
    s.home_branch_id,
    s.preferred_currency_id,
    s.customer_since
);


/* Customer 4 - USD preference */
MERGE INTO dim_customer d
USING (
    SELECT
        'CUST000004' AS customer_number,
        'SRC_CUST_000004' AS source_customer_id,
        'INDIVIDUAL' AS customer_type,
        'PRIVATE_BANKING' AS customer_segment,
        'Emeka' AS first_name,
        'Nwosu' AS last_name,
        'Emeka Nwosu' AS full_name,
        DATE '1978-01-17' AS date_of_birth,
        'M' AS gender,
        '08094567890' AS mobile_number,
        'emeka.nwosu@example.com' AS email_address,
        'Enugu' AS city,
        'Enugu' AS state,
        'Nigeria' AS country,
        3 AS kyc_level,
        'MEDIUM' AS risk_rating,
        30 AS customer_risk_score,
        'N' AS pep_flag,
        'N' AS blacklisted_flag,
        2 AS home_branch_id,
        2 AS preferred_currency_id,
        DATE '2016-08-20' AS customer_since
    FROM dual
) s
ON (d.customer_number = s.customer_number)

WHEN NOT MATCHED THEN
INSERT
(
    customer_number,
    source_customer_id,
    customer_type,
    customer_segment,
    first_name,
    last_name,
    full_name,
    date_of_birth,
    gender,
    mobile_number,
    email_address,
    city,
    state,
    country,
    kyc_level,
    risk_rating,
    customer_risk_score,
    pep_flag,
    blacklisted_flag,
    home_branch_id,
    preferred_currency_id,
    customer_since
)
VALUES
(
    s.customer_number,
    s.source_customer_id,
    s.customer_type,
    s.customer_segment,
    s.first_name,
    s.last_name,
    s.full_name,
    s.date_of_birth,
    s.gender,
    s.mobile_number,
    s.email_address,
    s.city,
    s.state,
    s.country,
    s.kyc_level,
    s.risk_rating,
    s.customer_risk_score,
    s.pep_flag,
    s.blacklisted_flag,
    s.home_branch_id,
    s.preferred_currency_id,
    s.customer_since
);

COMMIT;
