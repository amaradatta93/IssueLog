from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    def as_dict(self):
        return {
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
            'id': self.id
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
