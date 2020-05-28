from wtforms import Form, StringField, RadioField, SelectField, DateField, TextAreaField
from wtforms.widgets import TextArea


class IssueForm(Form):
    customer_name = StringField()
    company = StringField()
    source = RadioField('Source', choices=[('Phone', 'Phone'), ('E-Mail', 'E-Mail')])
    e_mail = StringField()
    phone_number = StringField()
    issue_report_date = DateField()
    issue_description = TextAreaField('Issue Description')
    domain = RadioField('Domain', choices=[('Fleet', 'Fleet'), ('HOS', 'HOS')])
    priority = SelectField('Priority', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    support_engineer = SelectField('Support Engineer',
                                   choices=[('Amara', 'Amara'), ('Ravi', 'Ravi'), ('Sridhar', 'Sridhar')])
    issue_fixed_date = DateField()
    status = SelectField('Status', choices=[('Working', 'Working'), ('Fixed', 'Fixed')])
    support_engineer_comments = TextAreaField('Support Engineer Comments')
