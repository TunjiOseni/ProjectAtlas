-- ============================================================
-- ProjectAtlas
-- Seed: DIM_ACCOUNT_OFFICER
-- Source: account_officer_or_rm(2).xls
-- Idempotent MERGE seed
--
-- Initial DIM_BRANCH mappings preserved:
--   BRANCH_CODE '0018' -> BRANCH_ID 1
--   BRANCH_CODE '0019' -> BRANCH_ID 2
--
-- For SOL_ID values not yet present in DIM_BRANCH, BRANCH_ID
-- remains NULL. No branch ID is invented.
-- ============================================================

MERGE INTO dim_account_officer tgt
USING (
    SELECT
        'D94RB' AS account_officer_code,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_name,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_email,
        CAST(NULL AS VARCHAR2(30)) AS account_officer_phone,
        '0' AS officer_status,
        (SELECT branch_id FROM dim_branch WHERE branch_code = '0494') AS branch_id,
        TIMESTAMP '2020-06-01 12:06:30' AS created_date,
        TIMESTAMP '2022-04-01 17:14:33' AS last_modified_date
    FROM dual
) src
ON (tgt.account_officer_code = src.account_officer_code)
WHEN MATCHED THEN
    UPDATE SET
        tgt.account_officer_name  = src.account_officer_name,
        tgt.account_officer_email = src.account_officer_email,
        tgt.account_officer_phone = src.account_officer_phone,
        tgt.officer_status        = src.officer_status,
        tgt.branch_id             = src.branch_id,
        tgt.last_modified_date    = src.last_modified_date
WHEN NOT MATCHED THEN
    INSERT
    (
        account_officer_code,
        account_officer_name,
        account_officer_email,
        account_officer_phone,
        officer_status,
        branch_id,
        created_date,
        last_modified_date
    )
    VALUES
    (
        src.account_officer_code,
        src.account_officer_name,
        src.account_officer_email,
        src.account_officer_phone,
        src.officer_status,
        src.branch_id,
        src.created_date,
        src.last_modified_date
    );

MERGE INTO dim_account_officer tgt
USING (
    SELECT
        'D711A' AS account_officer_code,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_name,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_email,
        CAST(NULL AS VARCHAR2(30)) AS account_officer_phone,
        '9' AS officer_status,
        (SELECT branch_id FROM dim_branch WHERE branch_code = '0471') AS branch_id,
        TIMESTAMP '2020-06-01 12:06:30' AS created_date,
        TIMESTAMP '2022-01-07 12:55:30' AS last_modified_date
    FROM dual
) src
ON (tgt.account_officer_code = src.account_officer_code)
WHEN MATCHED THEN
    UPDATE SET
        tgt.account_officer_name  = src.account_officer_name,
        tgt.account_officer_email = src.account_officer_email,
        tgt.account_officer_phone = src.account_officer_phone,
        tgt.officer_status        = src.officer_status,
        tgt.branch_id             = src.branch_id,
        tgt.last_modified_date    = src.last_modified_date
WHEN NOT MATCHED THEN
    INSERT
    (
        account_officer_code,
        account_officer_name,
        account_officer_email,
        account_officer_phone,
        officer_status,
        branch_id,
        created_date,
        last_modified_date
    )
    VALUES
    (
        src.account_officer_code,
        src.account_officer_name,
        src.account_officer_email,
        src.account_officer_phone,
        src.officer_status,
        src.branch_id,
        src.created_date,
        src.last_modified_date
    );

MERGE INTO dim_account_officer tgt
USING (
    SELECT
        'A622A' AS account_officer_code,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_name,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_email,
        CAST(NULL AS VARCHAR2(30)) AS account_officer_phone,
        '9' AS officer_status,
        (SELECT branch_id FROM dim_branch WHERE branch_code = '0162') AS branch_id,
        TIMESTAMP '2020-06-01 12:06:30' AS created_date,
        TIMESTAMP '2022-01-07 12:56:40' AS last_modified_date
    FROM dual
) src
ON (tgt.account_officer_code = src.account_officer_code)
WHEN MATCHED THEN
    UPDATE SET
        tgt.account_officer_name  = src.account_officer_name,
        tgt.account_officer_email = src.account_officer_email,
        tgt.account_officer_phone = src.account_officer_phone,
        tgt.officer_status        = src.officer_status,
        tgt.branch_id             = src.branch_id,
        tgt.last_modified_date    = src.last_modified_date
WHEN NOT MATCHED THEN
    INSERT
    (
        account_officer_code,
        account_officer_name,
        account_officer_email,
        account_officer_phone,
        officer_status,
        branch_id,
        created_date,
        last_modified_date
    )
    VALUES
    (
        src.account_officer_code,
        src.account_officer_name,
        src.account_officer_email,
        src.account_officer_phone,
        src.officer_status,
        src.branch_id,
        src.created_date,
        src.last_modified_date
    );

MERGE INTO dim_account_officer tgt
USING (
    SELECT
        'C47RA' AS account_officer_code,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_name,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_email,
        CAST(NULL AS VARCHAR2(30)) AS account_officer_phone,
        '9' AS officer_status,
        (SELECT branch_id FROM dim_branch WHERE branch_code = '0347') AS branch_id,
        TIMESTAMP '2020-06-01 12:06:30' AS created_date,
        TIMESTAMP '2022-01-07 12:58:44' AS last_modified_date
    FROM dual
) src
ON (tgt.account_officer_code = src.account_officer_code)
WHEN MATCHED THEN
    UPDATE SET
        tgt.account_officer_name  = src.account_officer_name,
        tgt.account_officer_email = src.account_officer_email,
        tgt.account_officer_phone = src.account_officer_phone,
        tgt.officer_status        = src.officer_status,
        tgt.branch_id             = src.branch_id,
        tgt.last_modified_date    = src.last_modified_date
WHEN NOT MATCHED THEN
    INSERT
    (
        account_officer_code,
        account_officer_name,
        account_officer_email,
        account_officer_phone,
        officer_status,
        branch_id,
        created_date,
        last_modified_date
    )
    VALUES
    (
        src.account_officer_code,
        src.account_officer_name,
        src.account_officer_email,
        src.account_officer_phone,
        src.officer_status,
        src.branch_id,
        src.created_date,
        src.last_modified_date
    );

MERGE INTO dim_account_officer tgt
USING (
    SELECT
        'B81RC' AS account_officer_code,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_name,
        CAST(NULL AS VARCHAR2(150)) AS account_officer_email,
        CAST(NULL AS VARCHAR2(30)) AS account_officer_phone,
        '9' AS officer_status,
        (SELECT branch_id FROM dim_branch WHERE branch_code = '0281') AS branch_id,
        TIMESTAMP '2020-06-01 12:06:30' AS created_date,
        TIMESTAMP '2022-01-07 13:00:25' AS last_modified_date
    FROM dual
) src
ON (tgt.account_officer_code = src.account_officer_code)
WHEN MATCHED THEN
    UPDATE SET
        tgt.account_officer_name  = src.account_officer_name,
        tgt.account_officer_email = src.account_officer_email,
        tgt.account_officer_phone = src.account_officer_phone,
        tgt.officer_status        = src.officer_status,
        tgt.branch_id             = src.branch_id,
        tgt.last_modified_date    = src.last_modified_date
WHEN NOT MATCHED THEN
    INSERT
    (
        account_officer_code,
        account_officer_name,
        account_officer_email,
        account_officer_phone,
        officer_status,
        branch_id,
        created_date,
        last_modified_date
    )
    VALUES
    (
        src.account_officer_code,
        src.account_officer_name,
        src.account_officer_email,
        src.account_officer_phone,
        src.officer_status,
        src.branch_id,
        src.created_date,
        src.last_modified_date
    );

COMMIT;
