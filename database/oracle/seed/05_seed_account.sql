/* =========================================================
   PROJECT ATLAS
   DIM_ACCOUNT SEED DATA
   ========================================================= */


/* =========================================================
   ACCOUNT 1
   Adebayo Johnson - NGN Savings
   ========================================================= */

INSERT INTO dim_account
(
    account_number,
    source_acid,
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
    ledger_balance
)
SELECT
    '0018000001',
    'SRC_ACID_000001',
    c.customer_id,
    s.schm_id,
    1,
    1,
    'ADEBAYO OLUWASEUN JOHNSON',
    'SBA',
    'PERSONAL',
    'ACTIVE',
    DATE '2019-06-15',
    250000.00,
    250000.00
FROM dim_customer c
CROSS JOIN dim_schm_code s
WHERE c.customer_number = 'CUST000001'
  AND s.schm_code = 'SBAGEN'
  AND NOT EXISTS
  (
      SELECT 1
      FROM dim_account a
      WHERE a.account_number = '001800000001'
  );


/* =========================================================
   ACCOUNT 2
   Chidinma Okafor - NGN Savings
   ========================================================= */

INSERT INTO dim_account
(
    account_number,
    source_acid,
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
    ledger_balance
)
SELECT
    '0019000002',
    'SRC_ACID_000002',
    c.customer_id,
    s.schm_id,
    2,
    1,
    'CHIDINMA OKAFOR',
    'SBA',
    'PERSONAL',
    'ACTIVE',
    DATE '2020-02-10',
    175000.00,
    175000.00
FROM dim_customer c
CROSS JOIN dim_schm_code s
WHERE c.customer_number = 'CUST000002'
  AND s.schm_code = 'SBAGEN'
  AND NOT EXISTS
  (
      SELECT 1
      FROM dim_account a
      WHERE a.account_number = '001900000002'
  );


/* =========================================================
   ACCOUNT 3
   Atlas Foods Limited - NGN Current
   ========================================================= */

INSERT INTO dim_account
(
    account_number,
    source_acid,
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
    overdraft_limit
)
SELECT
    '0018000003',
    'SRC_ACID_000003',
    c.customer_id,
    s.schm_id,
    1,
    1,
    'ATLAS FOODS LIMITED',
    'CAA',
    'BUSINESS',
    'ACTIVE',
    DATE '2018-11-01',
    3500000.00,
    3500000.00,
    1000000.00
FROM dim_customer c
CROSS JOIN dim_schm_code s
WHERE c.customer_number = 'CUST000003'
  AND s.schm_code = 'CAGEN'
  AND NOT EXISTS
  (
      SELECT 1
      FROM dim_account a
      WHERE a.account_number = '001800000003'
  );


/* =========================================================
   ACCOUNT 4
   Emeka Nwosu - USD Savings
   ========================================================= */

INSERT INTO dim_account
(
    account_number,
    source_acid,
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
    ledger_balance
)
SELECT
    '0019000004',
    'SRC_ACID_000004',
    c.customer_id,
    s.schm_id,
    2,
    2,
    'EMEKA NWOSU',
    'SBA',
    'PERSONAL',
    'ACTIVE',
    DATE '2016-08-20',
    5000.00,
    5000.00
FROM dim_customer c
CROSS JOIN dim_schm_code s
WHERE c.customer_number = 'CUST000004'
  AND s.schm_code = 'SBAGEN'
  AND NOT EXISTS
  (
      SELECT 1
      FROM dim_account a
      WHERE a.account_number = '001900000004'
  );

COMMIT;

SELECT
    account_id,
    account_number,
    source_acid,
    account_name,
    account_type,
    branch_id,
    currency_id,
    available_balance
FROM dim_account
ORDER BY account_id;


