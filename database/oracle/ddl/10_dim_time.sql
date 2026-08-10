CREATE TABLE dim_time
(
    time_id                 NUMBER(6) PRIMARY KEY,
    time_value              DATE NOT NULL,
    hour_number             NUMBER(2) NOT NULL,
    minute_number           NUMBER(2) NOT NULL,
    second_number           NUMBER(2) NOT NULL,
    hour_24                 NUMBER(2) NOT NULL,
    hour_12                 NUMBER(2) NOT NULL,
    am_pm                   VARCHAR2(2) NOT NULL,
    time_label              VARCHAR2(8) NOT NULL,
    time_period             VARCHAR2(20),
    created_by              VARCHAR2(50) DEFAULT USER,
    created_date            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_dim_time_value
        UNIQUE (time_value),
    CONSTRAINT chk_dim_time_am_pm
        CHECK (am_pm IN ('AM', 'PM'))
);
