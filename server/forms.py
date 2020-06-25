from wtforms import Form, StringField, RadioField, SelectField, DateField, TextAreaField, FileField


class IssueForm(Form):
    customer_name = StringField()
    company = StringField()
    source = RadioField()
    e_mail = StringField()
    phone_number = StringField()
    issue_report_date = DateField()
    issue_description = TextAreaField()
    domain = RadioField()
    priority = SelectField()
    assigned_to = SelectField()
    issue_fixed_date = DateField()
    status = SelectField()
    support_engineer_comments = TextAreaField()
    issue_file = FileField()
