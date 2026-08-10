CREATE TABLE dim_date
(
    date_id                 NUMBER PRIMARY KEY,
    calendar_date           DATE NOT NULL,
    day_number              NUMBER(2) NOT NULL,
    day_name                VARCHAR2(10) NOT NULL,
    day_of_week             NUMBER(1) NOT NULL,
    day_of_year             NUMBER(3) NOT NULL,
    week_of_year            NUMBER(2) NOT NULL,
    month_number            NUMBER(2) NOT NULL,
    month_name              VARCHAR2(10) NOT NULL,
    month_short_name        VARCHAR2(3) NOT NULL,
    quarter_number          NUMBER(1) NOT NULL,
    quarter_name            VARCHAR2(2) NOT NULL,
    year_number             NUMBER(4) NOT NULL,
    is_weekend              CHAR(1) DEFAULT 'N' NOT NULL,
    is_month_start          CHAR(1) DEFAULT 'N' NOT NULL,
    is_month_end            CHAR(1) DEFAULT 'N' NOT NULL,
    is_quarter_end          CHAR(1) DEFAULT 'N' NOT NULL,
    is_year_end              CHAR(1) DEFAULT 'N' NOT NULL,
    financial_year          NUMBER(4),
    created_by              VARCHAR2(50) DEFAULT USER,
    created_date            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_dim_date_weekend
        CHECK (is_weekend IN ('Y', 'N')),
    CONSTRAINT chk_dim_date_month_start
        CHECK (is_month_start IN ('Y', 'N')),
    CONSTRAINT chk_dim_date_month_end
        CHECK (is_month_end IN ('Y', 'N')),
    CONSTRAINT chk_dim_date_quarter_end
        CHECK (is_quarter_end IN ('Y', 'N')),
    CONSTRAINT chk_dim_date_year_end
        CHECK (is_year_end IN ('Y', 'N')),
    CONSTRAINT uk_dim_date_calendar_date
        UNIQUE (calendar_date)
);
