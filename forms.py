from wtforms import Form, StringField, RadioField, SelectField, DateField
from wtforms.widgets import TextArea


class IssueForm(Form):
    customer_name = StringField()
    company = StringField()
    source = RadioField('source', choices=[('Phone', 'Phone'), ('E-Mail', 'E-Mail')])
    e_mail = StringField()
    phone_number = StringField()
    issue_report_date = DateField()
    issue_description = TextArea()
    domain = RadioField('domain', choices=[('Fleet', 'Fleet'), ('HOS', 'HOS')])
    priority = SelectField('priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    support_engineer = SelectField('support_engineer', choices=[('Amara', 'Amara'), ('Ravi', 'Ravi'), ('Sridhar', 'Sridhar')])
    issue_fixed_date = DateField()
    status = SelectField('status', choices=[('Working', 'Working'), ('Fixed', 'Fixed')])
    support_engineer_comments = TextArea()
