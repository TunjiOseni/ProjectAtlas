from etl.extract.extract_branch import extract_branches


def transform_branches(branches):
    transformed = []

    for branch in branches:
        transformed.append({
            "branch_id": int(branch["BRANCH_ID"]),
            "branch_code": branch["BRANCH_CODE"],
            "branch_name": branch["BRANCH_NAME"],
            "branch_status": branch["BRANCH_STATUS"],
        })

    return transformed


if __name__ == "__main__":
    branches = extract_branches()
    transformed = transform_branches(branches)

    print(f"Transformed {len(transformed)} branches")

    for branch in transformed:
        print(branch)
