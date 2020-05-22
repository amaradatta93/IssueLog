from flask import Flask, render_template, request
from flask.views import MethodView, View

from config import app
from db import Issues
from forms import IssueForm


class Main(MethodView):

    def get(self):
        issue_json_data = Issues.query.all()
        return render_template('dashboard.html', issues=issue_json_data)

    def post(self):
        data = IssueForm(request.form)

        if data.validate():
            import pprint
            pprint.pprint(data)
            return request.form
        else:
            print(data.errors)
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
        pass
        issue_json_data = Issues.query.filter(Issues.status == 'Working')
        return render_template('dashboard.html', issues=issue_json_data)


app.add_url_rule('/unresolved', view_func=Unresolved.as_view('unresolved'))


class Search(MethodView):

    def get(self):
        pass
        search_param = request.args.get('search_param')
        issue_json_data = Issues.query.filter(Issues.issue_description.contains(search_param))
        import pprint
        pprint.pprint(issue_json_data)
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
