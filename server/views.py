from flask import render_template, request, Blueprint, flash, url_for, jsonify
from flask.views import MethodView
from flask_cors import CORS
from werkzeug.utils import redirect

from server.auth import login_required
from server.db import Issues, IssuesSchema, db
from server.forms import IssueForm

dashboard = Blueprint('dashboard', __name__)
CORS(dashboard)
issues = Blueprint('issues', __name__)
CORS(issues)

issue_schema = IssuesSchema()
issues_schema = IssuesSchema(many=True)


class Main(MethodView):
    # decorators = [login_required]

    def get(self, issue_id=None):
        if issue_id:
            response = Issues.query.get(issue_id)
            issue_json_data = issue_schema.dump(response)
            return jsonify(issue=issue_json_data)
        response = Issues.query.all()
        issue_json_data = issues_schema.dump(response)
        return jsonify(issues=issue_json_data)

    def post(self):
        form = IssueForm(request.form)

        if form.validate():
            issue = Issues()
            issue.customer_name = form.customer_name.data
            issue.company = form.company.data
            issue.source = form.source.data
            issue.email = form.e_mail.data
            issue.phone = form.phone_number.data
            issue.issue_report_date = form.issue_report_date.data
            issue.issue_description = form.issue_description.data
            issue.domain = form.domain.data
            issue.priority = form.priority.data
            issue.support_engineer = form.support_engineer.data
            issue.issue_fix_date = form.issue_fixed_date.data
            issue.status = form.status.data
            issue.support_engineer_comments = form.support_engineer_comments.data
            db.session.add(issue)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            flash(form.errors)
            return redirect(url_for('dashboard.add_issue'))


dashboard.add_url_rule('/', view_func=Main.as_view('main'))
dashboard.add_url_rule('/<int:issue_id>', view_func=Main.as_view('vis'))


class Resolved(MethodView):
    # decorators = [login_required]

    def get(self):
        response = Issues.query.filter(Issues.status == 'Fixed')
        issue_json_data = issues_schema.dump(response)
        return jsonify(issues=issue_json_data)


dashboard.add_url_rule('/resolved', view_func=Resolved.as_view('resolved'))


class Unresolved(MethodView):
    # decorators = [login_required]

    def get(self):
        response = Issues.query.filter(Issues.status == 'Working')
        issue_json_data = issues_schema.dump(response)
        return jsonify(issues=issue_json_data)


dashboard.add_url_rule('/unresolved', view_func=Unresolved.as_view('unresolved'))


class Search(MethodView):
    # decorators = [login_required]

    def get(self):
        search_param = request.args.get('search_param')
        response = Issues.query.filter(Issues.issue_description.contains(search_param))
        issue_json_data = issues_schema.dump(response)
        return jsonify(issues=issue_json_data)


dashboard.add_url_rule('/search', view_func=Search.as_view('search'))


class Modify(MethodView):
    decorators = [login_required]

    def post(self, issue_id):
        form = IssueForm(request.form)

        if form.validate():
            try:
                issue = Issues.query.get(issue_id)
                issue.customer_name = form.customer_name.data
                issue.company = form.company.data
                issue.source = form.source.data
                issue.email = form.e_mail.data
                issue.phone = form.phone_number.data
                issue.issue_report_date = form.issue_report_date.data
                issue.issue_description = form.issue_description.data
                issue.domain = form.domain.data
                issue.priority = form.priority.data
                issue.support_engineer = form.support_engineer.data
                issue.issue_fix_date = form.issue_fixed_date.data
                issue.status = form.status.data
                issue.support_engineer_comments = form.support_engineer_comments.data
                db.session.add(issue)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(e)
                flash(e)
                return redirect(url_for('issues.edit_issue', issue_id=issue_id))

        else:
            print(form.errors)
            flash(form.errors)
            return redirect(url_for('issues.edit_issue', issue_id=issue_id))


issues.add_url_rule('/modify/<int:issue_id>', view_func=Modify.as_view('modify'))


class Delete(MethodView):
    decorators = [login_required]

    def post(self, issue_id):
        try:
            issue = Issues.query.get(issue_id)
            db.session.delete(issue)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            flash(e)
            return redirect(url_for('issues.edit_issue', issue_id=issue_id))


issues.add_url_rule('/delete/<int:issue_id>', view_func=Delete.as_view('delete'))


class IssueOperation(MethodView):
    decorators = [login_required]

    def get(self, issue_id=None):
        if issue_id:
            issue_json_data = Issues.query.get(issue_id).as_dict()
            form = IssueForm(formdata=request.form, obj=issue_json_data)
            return render_template('add-edit/edit_issue.html', issues=issue_json_data, form=form)
        return render_template('add-edit/add_issue.html')


dashboard.add_url_rule('/add-issue', view_func=IssueOperation.as_view('add_issue'))
issues.add_url_rule('/edit-issue/<int:issue_id>', view_func=IssueOperation.as_view('edit_issue'))
