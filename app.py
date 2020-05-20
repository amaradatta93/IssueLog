import os
import pprint

from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql.init_app(app)


@app.route("/")
def main():
    row_headers = ["Customer Name", "Company", "Source", "E - mail", "Phone", "Issue Report Date",
                   "Issue Description", "Domain", "Priority", "Support Engineer", "Issue Fix Date",
                   "Status", "Support Engineer Comments", "id"]
    issue_json_data = []
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('''
                        select * from issues
                    ''')
    issue_list = cursor.fetchall()
    conn.close()
    for result in issue_list:
        issue_json_data.append(dict(zip(row_headers, result)))
    return render_template('dashboard.html', issues=issue_json_data)


if __name__ == "__main__":
    app.run()
