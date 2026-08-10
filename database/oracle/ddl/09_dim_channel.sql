/*
=========================================================
Project      : Project Atlas
Module       : Transaction Engine
Object Name  : DIM_CHANNEL
Object Type  : Table
Author       : Olatunji Oseni
Description  : Stores transaction channel reference data
=========================================================
*/
CREATE TABLE dim_channel
(
    channel_code           VARCHAR2(5)      NOT NULL,
    channel_name           VARCHAR2(50)     NOT NULL,
    description            VARCHAR2(200),
    system_defined         CHAR(1)          DEFAULT 'Y',
    display_order          NUMBER(3),
    status                 VARCHAR2(20)     DEFAULT 'ACTIVE',
    created_by             VARCHAR2(50)     DEFAULT USER,
    created_date           TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    modified_by            VARCHAR2(50),
    last_modified_date     TIMESTAMP,
    CONSTRAINT pk_dim_channel
        PRIMARY KEY (channel_code),
    CONSTRAINT chk_dim_channel_status
        CHECK (status IN ('ACTIVE','INACTIVE')),     
    CONSTRAINT chk_dim_channel_system
        CHECK (system_defined IN ('Y','N'))
);
