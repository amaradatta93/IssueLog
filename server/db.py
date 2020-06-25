from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class Issues(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    issue_report_date = db.Column(db.String(10), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(255), nullable=False)
    assigned_to = db.Column(db.String(255), nullable=False)
    issue_fix_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    support_engineer_comments = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    issue_file = db.Column(db.String(255), nullable=True)

    def as_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'company': self.company,
            'source': self.source,
            'email': self.email,
            'phone': self.phone,
            'issue_report_date': str(self.issue_report_date),
            'issue_description': self.issue_description,
            'domain': self.domain,
            'priority': self.priority,
            'support_engineer': self.support_engineer,
            'issue_fix_date': str(self.issue_fix_date),
            'status': self.status,
            'support_engineer_comments': self.support_engineer_comments,
            'issue_file': self.issue_file
        }


class IssueSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'customer_name', 'company', 'source', 'email', 'phone', 'issue_report_date', 'issue_description',
            'domain', 'priority', 'assigned_to', 'issue_fix_date', 'status', 'support_engineer_comments', 'issue_file'
        )


class IssuesSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'company', 'issue_report_date', 'issue_description', 'priority', 'domain',
            'assigned_to', 'status'
        )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False, unique=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'username', 'user_email'
        )


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
