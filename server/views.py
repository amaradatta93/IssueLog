from flask import request, Blueprint, jsonify, send_from_directory
from flask.views import MethodView
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.config import UPLOAD_FOLDER
from server.db import db, Issues, SupportEngineers, IssueSchema, IssuesSchema, SupportEngineersSchema
from server.forms import IssueForm
from server.utils import email_service, get_recipients, add_issue_email_body, edit_issue_email_body, \
    assign_customer_data_to_issue, delete_old_file_from_folder, save_file_to_folder, get_reminder_email_content

dashboard = Blueprint('dashboard', __name__)
support_engineers = Blueprint('support_engineers', __name__,  url_prefix='/support-engineers')
CORS(dashboard)
CORS(support_engineers)

issue_schema = IssueSchema()
issues_schema = IssuesSchema(many=True)
support_engineers_schema = SupportEngineersSchema(many=True)


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

        if request.method == "POST" and request.form:
            identity = get_jwt_identity()
            new_issue = IssueForm(request.form)
            issue = Issues()

            try:
                issue = assign_customer_data_to_issue(issue, new_issue)
                issue.user_id = identity['id']

                if request.files:
                    file = request.files['issue_file']
                    filename = save_file_to_folder(UPLOAD_FOLDER, file, str(new_issue.issue_report_date.data))
                    issue.issue_file = filename
                else:
                    issue.issue_file = None

                recipients = get_recipients(new_issue.assigned_to.data)
                email_body = add_issue_email_body(new_issue)
                subject = f"{identity['username']} has added an issue"
                email_service(recipients, email_body, subject)

                db.session.add(issue)
                db.session.commit()
                resp = jsonify(success=True)
                return resp
            except Exception as e:
                resp = jsonify(error=e)
                return resp

    def put(self, issue_id):

        if request.method == "PUT" and request.form:
            identity = get_jwt_identity()
            updated_issue = IssueForm(request.form)

            try:
                issue = Issues.query.get(issue_id)
                issue = assign_customer_data_to_issue(issue, updated_issue)

                if request.files:
                    file = request.files['issue_file']

                    if issue.issue_file:
                        delete_old_file_from_folder(UPLOAD_FOLDER, issue.issue_file)
                    filename = save_file_to_folder(UPLOAD_FOLDER, file, str(updated_issue.issue_report_date.data))
                    issue.issue_file = filename

                recipients = get_recipients(updated_issue.assigned_to.data)
                email_body = edit_issue_email_body(updated_issue, issue_id)
                subject = f"{identity['username']} has updated the ticket {issue_id}"
                email_service(recipients, email_body, subject)

                db.session.add(issue)
                db.session.commit()
                resp = jsonify(success=True)
                return resp
            except Exception as e:
                resp = jsonify(error=e)
                return resp

    def delete(self, issue_id):
        identity = get_jwt_identity()
        resp = jsonify(error='Not authorized. Please contact support team to delete')

        if request.method == "DELETE" and issue_id and identity['role'] == 'admin':
            try:
                issue = Issues.query.get(issue_id)

                if issue.issue_file:
                    delete_old_file_from_folder(UPLOAD_FOLDER, issue.issue_file)

                db.session.delete(issue)
                db.session.commit()
                resp = jsonify(success=True)
                return resp
            except Exception as e:
                resp = jsonify(error=e)
                return resp

        return resp


dashboard.add_url_rule('/', view_func=Main.as_view('main'))
dashboard.add_url_rule('/issue/<int:issue_id>', view_func=Main.as_view('view_issue'))
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


class FileView(MethodView):
    decorators = [jwt_required]

    def get(self):
        if request.method == "GET":
            file_name = request.args.get('issue_file_name')
            resp = send_from_directory(UPLOAD_FOLDER, file_name, as_attachment=True)
            return resp


dashboard.add_url_rule('/file', view_func=FileView.as_view('issue_file_view'))


class IssueReminder(MethodView):
    decorators = [jwt_required]

    def post(self):
        resp = jsonify(reminder=False)
        identity = get_jwt_identity()

        if request.method == "POST":
            reminder_data = request.get_json()
            ticket, assigned_to = reminder_data['id'], reminder_data['assigned_to']
            recipients = get_recipients(assigned_to)
            content = get_reminder_email_content(ticket, identity['username'])
            subject = f"Reminder email from {identity['username']}"
            email_service(recipients, content, subject)
            resp = jsonify(reminder=True)

        return resp


dashboard.add_url_rule('/remind', view_func=IssueReminder.as_view('issue_reminder_email'))


class User(MethodView):
    decorators = [jwt_required]

    def get(self):
        identity = get_jwt_identity()

        if request.method == "GET":
            try:
                response = SupportEngineers.query.all()
                support_engineers_json_data = support_engineers_schema.dump(response)
                return jsonify(support_engineers=support_engineers_json_data)
            except Exception as e:
                return jsonify(error=e)

    def post(self):
        identity = get_jwt_identity()

        if request.method == "POST" and identity['role'] == 'admin':
            new_support_engineer = request.get_json()
            engineers = SupportEngineers()

            try:
                name = new_support_engineer['support_engineer_name']
                if not engineers.query.filter_by(support_engineer_name=name).first():
                    engineers.support_engineer_name = name
                    db.session.add(engineers)
                    db.session.commit()
                    resp = jsonify(success=True)
                else:
                    resp = jsonify(error="Support engineer already exists")
                return resp
            except Exception as e:
                resp = jsonify(error=e)
                return resp

    def delete(self, support_engineer_id):
        identity = get_jwt_identity()

        if request.method == "DELETE" and support_engineer_id and identity['role'] == 'admin':

            try:
                support_engineer = SupportEngineers.query.get(support_engineer_id)
                db.session.delete(support_engineer)
                db.session.commit()
                resp = jsonify(success=True)
                return resp
            except Exception as e:
                resp = jsonify(error=e)
                return resp


support_engineers.add_url_rule('/', view_func=User.as_view('get_engineers'))
support_engineers.add_url_rule('/add', view_func=User.as_view('add_engineers'))
support_engineers.add_url_rule('/delete/<int:support_engineer_id>', view_func=User.as_view('delete_engineers'))
