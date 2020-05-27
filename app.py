from flask import Flask, render_template, request
from flask.views import MethodView, View
from werkzeug.utils import redirect

from config import app
from db import Issues, db
from forms import IssueForm


class Main(MethodView):

    def get(self):
        issue_json_data = Issues.query.all()
        return render_template('dashboard.html', issues=issue_json_data)

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
            return redirect('')
        else:
            print(form.errors)
            return 'Failed'

    def patch(self):
        pass

    def delete(self):
        pass


app.add_url_rule('/', view_func=Main.as_view(''))


class Resolved(MethodView):

    def get(self):
        issue_json_data = Issues.query.filter(Issues.status == 'Fixed')
        return render_template('dashboard.html', issues=issue_json_data)


app.add_url_rule('/resolved', view_func=Resolved.as_view('resolved'))


class Unresolved(MethodView):

    def get(self):
        issue_json_data = Issues.query.filter(Issues.status == 'Working')
        return render_template('dashboard.html', issues=issue_json_data)


app.add_url_rule('/unresolved', view_func=Unresolved.as_view('unresolved'))


class Search(MethodView):

    def get(self):
        search_param = request.args.get('search_param')
        issue_json_data = Issues.query.filter(Issues.issue_description.contains(search_param))
        return render_template('dashboard.html', issues=issue_json_data)


app.add_url_rule('/search', view_func=Search.as_view('search'))


class RenderTemplateView(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)


app.add_url_rule('/add-issue', view_func=RenderTemplateView.as_view(
    'add_issue', template_name='add_issue.html'))

if __name__ == "__main__":
    app.run()
