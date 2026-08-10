CREATE TABLE dim_part_tran_type
(
    part_tran_type_code     CHAR(1)         NOT NULL,
    part_tran_type_name     VARCHAR2(20)    NOT NULL,
    description             VARCHAR2(200),
    status                  VARCHAR2(20)    DEFAULT 'ACTIVE',
    created_by              VARCHAR2(50)    DEFAULT USER,
    created_date            TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_dim_part_tran_type
        PRIMARY KEY (part_tran_type_code),

    CONSTRAINT chk_dim_part_tran_status
        CHECK (status IN ('ACTIVE','INACTIVE'))
);
