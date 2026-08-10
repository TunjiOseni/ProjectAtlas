INSERT ALL
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('BRN','Branch','Branch Teller','Y',1,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('ATM','ATM','Automated Teller Machine','Y',2,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('POS','POS','Point of Sale','Y',3,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('MOB','Mobile','Mobile Banking','Y',4,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('INT','Internet','Internet Banking','Y',5,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('USS','USSD','USSD Banking','Y',6,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('API','API','Application Programming Interface','Y',7,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('AGT','Agent','Agent Banking','Y',8,'ACTIVE',USER,CURRENT_TIMESTAMP)
INTO dim_channel
(channel_code,channel_name,description,system_defined,display_order,status,created_by,created_date)
VALUES
('BAT','Batch','Batch Processing','Y',9,'ACTIVE',USER,CURRENT_TIMESTAMP)
SELECT 1 FROM dual;
COMMIT;
