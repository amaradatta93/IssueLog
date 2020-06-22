from flask import request, Blueprint, flash, jsonify
from flask.views import MethodView
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.db import Issues, IssuesSchema, db

dashboard = Blueprint('dashboard', __name__)
CORS(dashboard)

issue_schema = IssuesSchema()
issues_schema = IssuesSchema(many=True)


class Main(MethodView):
    decorators = [jwt_required]

    def get(self, issue_id=None):

        if request.method == "GET":

            identity = get_jwt_identity()

            if issue_id:
                response = Issues.query.get(issue_id)
                issue_json_data = issue_schema.dump(response)
                return jsonify(issue=issue_json_data)

            if identity['role'] == 'admin':
                response = Issues.query.all()
                issue_json_data = issues_schema.dump(response)
                return jsonify(issues=issue_json_data)
            else:
                response = Issues.query.filter_by(user_id=identity['id']).all()
                issue_json_data = issues_schema.dump(response)
                return jsonify(issues=issue_json_data)

    def post(self):
        if request.method == "POST":
            identity = get_jwt_identity()
            new_issue = request.get_json()
            issue = Issues()

            issue.customer_name = new_issue['customer_name']
            issue.company = new_issue['company']
            issue.source = new_issue['source']
            issue.email = new_issue['e_mail']
            issue.phone = new_issue['phone_number']
            issue.issue_report_date = new_issue['issue_report_date']
            issue.issue_description = new_issue['issue_description']
            issue.domain = new_issue['domain']
            issue.priority = new_issue['priority']
            issue.assigned_to = new_issue['support_engineer']
            issue.issue_fix_date = new_issue['issue_fixed_date']
            issue.status = new_issue['status']
            issue.support_engineer_comments = new_issue['support_engineer_comments']
            issue.user_id = identity['id']
            db.session.add(issue)
            db.session.commit()
            resp = jsonify(success=True)
            return resp

    def put(self, issue_id):
        if request.method == "PUT" and issue_id:
            identity = get_jwt_identity()
            updated_issue = request.get_json()

            try:
                issue = Issues.query.get(issue_id)
                issue.customer_name = updated_issue['customer_name']
                issue.company = updated_issue['company']
                issue.source = updated_issue['source']
                issue.email = updated_issue['e_mail']
                issue.phone = updated_issue['phone_number']
                issue.issue_report_date = updated_issue['issue_report_date']
                issue.issue_description = updated_issue['issue_description']
                issue.domain = updated_issue['domain']
                issue.priority = updated_issue['priority']
                issue.assigned_to = updated_issue['support_engineer']
                issue.issue_fix_date = updated_issue['issue_fixed_date']
                issue.status = updated_issue['status']
                issue.support_engineer_comments = updated_issue['support_engineer_comments']
                issue.user_id = identity['id']
                db.session.add(issue)
                db.session.commit()
                resp = jsonify(success=True)
                return resp
            except Exception as e:
                print(e)
                flash(e)
                resp = jsonify(success=False)
                return resp

    def delete(self, issue_id):

        identity = get_jwt_identity()
        resp = jsonify(error='Not authorized')

        if request.method == "DELETE" and issue_id and identity['role'] == 'admin':

            try:
                issue = Issues.query.get(issue_id)
                db.session.delete(issue)
                db.session.commit()
                resp = jsonify(success=True)
                return resp
            except Exception as e:
                print(e)
                flash(e)
                resp = jsonify(success=False)
                return resp
        return resp


dashboard.add_url_rule('/', view_func=Main.as_view('main'))
dashboard.add_url_rule('/<int:issue_id>', view_func=Main.as_view('issue'))
dashboard.add_url_rule('/add-issue', view_func=Main.as_view('add_issue'))
dashboard.add_url_rule('/edit/<int:issue_id>', view_func=Main.as_view('edit_issue'))
dashboard.add_url_rule('/delete/<int:issue_id>', view_func=Main.as_view('delete_issue'))


class Search(MethodView):
    decorators = [jwt_required]

    def get(self):
        response = None
        identity = get_jwt_identity()
        search_param = request.args.get('search_param')

        if identity['role'] == 'admin':
            response = Issues.query.filter(Issues.issue_description.contains(search_param))

        elif identity['role'] == 'user':
            response = Issues.query.filter((Issues.issue_description.contains(search_param))
                                       & (Issues.user_id == identity['id']))

        issue_json_data = issues_schema.dump(response)
        return jsonify(issues=issue_json_data)


dashboard.add_url_rule('/search', view_func=Search.as_view('search'))
