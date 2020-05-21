import os

from flask import Flask, render_template

from utils import get_data_from_db, parse_db_data_as_json

app = Flask(__name__)


@app.route("/")
def main():
    statement = '''select * from issues'''
    issue_list = get_data_from_db(statement)
    issue_json_data = parse_db_data_as_json(issue_list)
    return render_template('dashboard.html', issues=issue_json_data)


@app.route("/resolved")
def resolved():
    statement = '''select * from issues where status="Fixed"'''
    issue_list = get_data_from_db(statement)
    issue_json_data = parse_db_data_as_json(issue_list)
    return render_template('dashboard.html', issues=issue_json_data)


@app.route("/unresolved")
def unresolved():
    statement = '''select * from issues where status="Working"'''
    issue_list = get_data_from_db(statement)
    issue_json_data = parse_db_data_as_json(issue_list)
    return render_template('dashboard.html', issues=issue_json_data)


@app.route("/search")
def search():
    pass


if __name__ == "__main__":
    app.run()
