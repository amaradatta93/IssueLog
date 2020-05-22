from flask_sqlalchemy import SQLAlchemy

from config import app

db = SQLAlchemy(app)


class Issues(db.Model):
    __tablename__ = 'issues'
    customer_name = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    issue_report_date = db.Column(db.String(10), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(255), nullable=False)
    support_engineer = db.Column(db.String(255), nullable=False)
    issue_fix_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    support_engineer_comments = db.Column(db.Text, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
