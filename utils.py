from db import mysql


def get_data_from_db(statement):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(statement)
    issue_list = cursor.fetchall()
    conn.close()
    return issue_list


def parse_db_data_as_json(data):
    row_headers = ["Customer Name", "Company", "Source", "E - mail", "Phone", "Issue Report Date",
                   "Issue Description", "Domain", "Priority", "Support Engineer", "Issue Fix Date",
                   "Status", "Support Engineer Comments", "id"]
    issue_json_data = []

    for result in data:
        issue_json_data.append(dict(zip(row_headers, result)))
    return issue_json_data
