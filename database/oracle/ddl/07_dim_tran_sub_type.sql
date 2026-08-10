/*
=========================================================
Project      : Project Atlas
Module       : Transaction Engine
Object Name  : DIM_TRAN_SUB_TYPE
Object Type  : Table
Author       : Olatunji Oseni
Description  : Stores transaction sub-type reference data
=========================================================
*/

CREATE TABLE dim_tran_sub_type
(
    tran_sub_type_code      VARCHAR2(2)     NOT NULL,

    tran_sub_type_name      VARCHAR2(50)    NOT NULL,

    description             VARCHAR2(200),

    system_defined          CHAR(1)         DEFAULT 'Y',

    display_order           NUMBER(3),

    status                  VARCHAR2(20)    DEFAULT 'ACTIVE',

    created_by              VARCHAR2(50)    DEFAULT USER,

    created_date            TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,

    modified_by             VARCHAR2(50),

    last_modified_date      TIMESTAMP,

    CONSTRAINT pk_dim_tran_sub_type
        PRIMARY KEY (tran_sub_type_code),

    CONSTRAINT chk_dim_tran_sub_type_status
        CHECK (status IN ('ACTIVE','INACTIVE')),

    CONSTRAINT chk_dim_tran_sub_type_system
        CHECK (system_defined IN ('Y','N'))
);
