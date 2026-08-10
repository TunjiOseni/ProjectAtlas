INSERT INTO dim_date
(
    date_id,
    calendar_date,
    day_number,
    day_name,
    day_of_week,
    day_of_year,
    week_of_year,
    month_number,
    month_name,
    month_short_name,
    quarter_number,
    quarter_name,
    year_number,
    is_weekend,
    is_month_start,
    is_month_end,
    is_quarter_end,
    is_year_end,
    financial_year
)
SELECT
    TO_NUMBER(TO_CHAR(dt, 'YYYYMMDD')) AS date_id,
    dt AS calendar_date,
    TO_NUMBER(TO_CHAR(dt, 'DD')) AS day_number,
    TO_CHAR(dt, 'DAY') AS day_name,
    TO_NUMBER(TO_CHAR(dt, 'D')) AS day_of_week,
    TO_NUMBER(TO_CHAR(dt, 'DDD')) AS day_of_year,
    TO_NUMBER(TO_CHAR(dt, 'IW')) AS week_of_year,
    TO_NUMBER(TO_CHAR(dt, 'MM')) AS month_number,
    TO_CHAR(dt, 'MONTH') AS month_name,
    TO_CHAR(dt, 'MON') AS month_short_name,
    TO_NUMBER(TO_CHAR(dt, 'Q')) AS quarter_number,
    'Q' || TO_CHAR(dt, 'Q') AS quarter_name,
    TO_NUMBER(TO_CHAR(dt, 'YYYY')) AS year_number,
    CASE
        WHEN TO_CHAR(dt, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH')
             IN ('SAT', 'SUN')
        THEN 'Y'
        ELSE 'N'
    END AS is_weekend,
    CASE
        WHEN TRUNC(dt, 'MM') = dt
        THEN 'Y'
        ELSE 'N'
    END AS is_month_start,
    CASE
        WHEN LAST_DAY(dt) = dt
        THEN 'Y'
        ELSE 'N'
    END AS is_month_end,
    CASE
        WHEN LAST_DAY(dt) = dt
         AND TO_CHAR(dt, 'MM') IN ('03', '06', '09', '12')
        THEN 'Y'
        ELSE 'N'
    END AS is_quarter_end,
    CASE
        WHEN LAST_DAY(dt) = dt
         AND TO_CHAR(dt, 'MM') = '12'
        THEN 'Y'
        ELSE 'N'
    END AS is_year_end,
    CASE
        WHEN TO_NUMBER(TO_CHAR(dt, 'MM')) >= 1
        THEN TO_NUMBER(TO_CHAR(dt, 'YYYY'))
    END AS financial_year
FROM
(
    SELECT DATE '2010-01-01' + LEVEL - 1 AS dt
    FROM dual
    CONNECT BY LEVEL <=
        DATE '2050-12-31' - DATE '2010-01-01' + 1
);
COMMIT;
