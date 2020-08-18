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
    issue_file = db.Column(db.String(255), nullable=True)
    domain = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(255), nullable=False)
    assigned_to = db.Column(db.String(255), nullable=False)
    support_engineer = db.Column(db.String(255), nullable=False)
    issue_fix_date = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(255), nullable=False)
    support_engineer_comments = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)


class IssueSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'customer_name', 'company', 'source', 'email', 'phone', 'issue_report_date', 'issue_description',
            'domain', 'priority', 'assigned_to', 'support_engineer', 'issue_fix_date', 'status',
            'support_engineer_comments', 'issue_file'
        )


class IssuesSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'company', 'issue_report_date', 'issue_description', 'priority', 'domain', 'support_engineer',
            'assigned_to', 'status'
        )


class SupportEngineers(db.Model):
    __tablename__ = 'support_engineers'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    support_engineer_name = db.Column(db.String(255), nullable=False)


class SupportEngineersSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'support_engineer_name'
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
