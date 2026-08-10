INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('CI','Customer Induced','Transaction initiated by customer',1);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('BI','Bank Induced','Transaction initiated by the bank',2);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('IP','Interest Payment','Interest credit or debit',3);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('NP','Normal Payment','Standard outgoing payment',4);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('NR','Normal Receipt','Standard incoming receipt',5);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('CH','Charges','Bank charges and fees',6);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('RV','Reversal','Transaction reversal',7);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('LN','Loan','Loan related transaction',8);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('FD','Fixed Deposit','Fixed deposit transaction',9);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('SI','Standing Instruction','Standing instruction execution',10);
INSERT INTO dim_tran_sub_type
(tran_sub_type_code, tran_sub_type_name, description, display_order)
VALUES
('FX','Foreign Exchange','Foreign exchange transaction',11);
COMMIT;


