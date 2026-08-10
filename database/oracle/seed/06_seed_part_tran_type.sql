INSERT INTO dim_part_tran_type
(part_tran_type_code, part_tran_type_name, description)
VALUES
('D',
 'Debit',
 'Debit leg of accounting transaction');
INSERT INTO dim_part_tran_type
(part_tran_type_code, part_tran_type_name, description)
VALUES
('C',
 'Credit',
 'Credit leg of accounting transaction');
COMMIT;
