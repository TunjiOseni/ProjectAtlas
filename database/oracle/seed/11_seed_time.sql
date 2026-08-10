INSERT INTO dim_time
(
    time_id,
    time_value,
    hour_number,
    minute_number,
    second_number,
    hour_24,
    hour_12,
    am_pm,
    time_label,
    time_period
)
SELECT
    TO_NUMBER(TO_CHAR(time_value, 'HH24MISS')) AS time_id,
    time_value,
    TO_NUMBER(TO_CHAR(time_value, 'HH24')) AS hour_number,
    TO_NUMBER(TO_CHAR(time_value, 'MI')) AS minute_number,
    TO_NUMBER(TO_CHAR(time_value, 'SS')) AS second_number,
    TO_NUMBER(TO_CHAR(time_value, 'HH24')) AS hour_24,
    TO_NUMBER(TO_CHAR(time_value, 'HH')) AS hour_12,
    TO_CHAR(time_value, 'AM') AS am_pm,
    TO_CHAR(time_value, 'HH24:MI:SS') AS time_label,
    CASE
        WHEN TO_NUMBER(TO_CHAR(time_value, 'HH24')) BETWEEN 0 AND 5
            THEN 'NIGHT'

        WHEN TO_NUMBER(TO_CHAR(time_value, 'HH24')) BETWEEN 6 AND 11
            THEN 'MORNING'

        WHEN TO_NUMBER(TO_CHAR(time_value, 'HH24')) BETWEEN 12 AND 17
            THEN 'AFTERNOON'

        ELSE 'EVENING'
    END AS time_period
FROM
(
    SELECT
        TRUNC(SYSDATE) + ((LEVEL - 1) / 86400) AS time_value
    FROM dual
    CONNECT BY LEVEL <= 86400
);
COMMIT;
