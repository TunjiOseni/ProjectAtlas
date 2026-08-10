/* =========================================================
   PROJECT ATLAS
   FACT_TRANSACTION TEST LOAD
   Grain:
   One source transaction part = one fact row
   ========================================================= */

INSERT INTO fact_transaction
(
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
    delete_flag
)
SELECT
    20260810,
    101500,
    20260810,
    a.account_id,
    a.customer_id,
    a.branch_id,
    a.currency_id,
    'TRF',
    'CI',
    'D',
    'MOB',
    NULL,
    'TXN000001',
    1,
    '100100',
    'TRANSFER',
    '001',
    25000,
    25000,
    NULL,
    1,
    'NGN',
    'REF000001',
    'Mobile transfer',
    'Transfer to beneficiary',
    'USER001',
    'USER001',
    'SUP001',
    DATE '2026-08-10',
    DATE '2026-08-10',
    DATE '2026-08-10',
    DATE '2026-08-10',
    DATE '2026-08-10',
    'POSTED',
    'N'
FROM dim_account a
WHERE a.account_number = '0018000001'
  AND NOT EXISTS
  (
      SELECT 1
      FROM fact_transaction f
      WHERE f.source_tran_id = 'TXN000001'
        AND f.part_tran_srl_num = 1
  );


INSERT INTO fact_transaction
(
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
    source_tran_id,
    part_tran_srl_num,
    transaction_amount,
    reference_amount,
    exchange_rate,
    reference_currency_code,
    reference_number,
    transaction_particular,
    entry_user_id,
    transaction_date,
    entry_date,
    posted_date,
    transaction_status,
    delete_flag
)
SELECT
    20260810,
    104500,
    20260810,
    a.account_id,
    a.customer_id,
    a.branch_id,
    a.currency_id,
    'POS',
    'CI',
    'D',
    'POS',
    'TXN000002',
    1,
    12500,
    12500,
    1,
    'NGN',
    'REF000002',
    'POS purchase',
    'SYSTEM',
    DATE '2026-08-10',
    DATE '2026-08-10',
    DATE '2026-08-10',
    'POSTED',
    'N'
FROM dim_account a
WHERE a.account_number = '0019000002'
  AND NOT EXISTS
  (
      SELECT 1
      FROM fact_transaction f
      WHERE f.source_tran_id = 'TXN000002'
        AND f.part_tran_srl_num = 1
  );


INSERT INTO fact_transaction
(
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
    source_tran_id,
    part_tran_srl_num,
    transaction_amount,
    reference_amount,
    exchange_rate,
    reference_currency_code,
    reference_number,
    transaction_particular,
    entry_user_id,
    transaction_date,
    entry_date,
    posted_date,
    transaction_status,
    delete_flag
)
SELECT
    20260810,
    113000,
    20260810,
    a.account_id,
    a.customer_id,
    a.branch_id,
    a.currency_id,
    'TRF',
    'NR',
    'C',
    'API',
    'TXN000003',
    1,
    750000,
    750000,
    1,
    'NGN',
    'REF000003',
    'Incoming business transfer',
    'SYSTEM',
    DATE '2026-08-10',
    DATE '2026-08-10',
    DATE '2026-08-10',
    'POSTED',
    'N'
FROM dim_account a
WHERE a.account_number = '0018000003'
  AND NOT EXISTS
  (
      SELECT 1
      FROM fact_transaction f
      WHERE f.source_tran_id = 'TXN000003'
        AND f.part_tran_srl_num = 1
  );

COMMIT;
