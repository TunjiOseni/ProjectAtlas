/* =========================================================
   PROJECT ATLAS
   FACT_TRANSACTION INDEXES
   ========================================================= */

CREATE INDEX idx_fact_tran_date
ON fact_transaction(date_id);

CREATE INDEX idx_fact_tran_account
ON fact_transaction(account_id);

CREATE INDEX idx_fact_tran_customer
ON fact_transaction(customer_id);

CREATE INDEX idx_fact_tran_branch
ON fact_transaction(transaction_branch_id);

CREATE INDEX idx_fact_tran_currency
ON fact_transaction(currency_id);

CREATE INDEX idx_fact_tran_type
ON fact_transaction(tran_type_code);

CREATE INDEX idx_fact_tran_channel
ON fact_transaction(channel_code);

CREATE INDEX idx_fact_tran_status
ON fact_transaction(transaction_status);

CREATE INDEX idx_fact_tran_tran_date
ON fact_transaction(transaction_date);
