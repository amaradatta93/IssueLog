import os

from flask import request, Blueprint, jsonify, send_from_directory
from flask.views import MethodView
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from server import UPLOAD_FOLDER
from server.db import db, Issues, IssueSchema, IssuesSchema
from server.forms import IssueForm

dashboard = Blueprint('dashboard', __name__)
CORS(dashboard)

issue_schema = IssueSchema()
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

        if request.method == "POST" and request.form:
            identity = get_jwt_identity()
            new_issue = IssueForm(request.form)
            issue = Issues()

            try:
                issue.customer_name = new_issue.customer_name.data
                issue.company = new_issue.company.data
                issue.source = new_issue.source.data
                issue.email = new_issue.e_mail.data
                issue.phone = new_issue.phone_number.data
                issue.issue_report_date = new_issue.issue_report_date.data
                issue.issue_description = new_issue.issue_description.data
                issue.domain = new_issue.domain.data
                issue.priority = new_issue.priority.data
                issue.assigned_to = new_issue.assigned_to.data
                issue.issue_fix_date = new_issue.issue_fixed_date.data
                issue.status = new_issue.status.data
                issue.support_engineer_comments = new_issue.support_engineer_comments.data
                issue.user_id = identity['id']

                if request.files:
                    file = request.files['issue_file']
                    name = secure_filename(file.filename)
                    filename = str(new_issue.issue_report_date.data) + '-' + name
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    issue.issue_file = filename
                else:
                    issue.issue_file = None

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
                issue.customer_name = updated_issue.customer_name.data
                issue.company = updated_issue.company.data
                issue.source = updated_issue.source.data
                issue.email = updated_issue.e_mail.data
                issue.phone = updated_issue.phone_number.data
                issue.issue_report_date = updated_issue.issue_report_date.data
                issue.issue_description = updated_issue.issue_description.data
                issue.domain = updated_issue.domain.data
                issue.priority = updated_issue.priority.data
                issue.assigned_to = updated_issue.assigned_to.data
                issue.issue_fix_date = updated_issue.issue_fixed_date.data
                issue.status = updated_issue.status.data
                issue.support_engineer_comments = updated_issue.support_engineer_comments.data
                issue.user_id = identity['id']

                if request.files:
                    os.remove(os.path.join(UPLOAD_FOLDER, issue.issue_file))
                    file = request.files['issue_file']
                    name = secure_filename(file.filename)
                    filename = str(updated_issue.issue_report_date.data) + '-' + name
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    issue.issue_file = filename

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
