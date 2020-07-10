import os
import random
import re
import string

from flask_mail import Message, Mail
from werkzeug.utils import secure_filename

MYSQL_URL_REGEX = re.compile(
    r'^mysql:\/\/(?P<username>.*?):(?P<password>.*?)@(?P<host>.*?)/(?P<db>.*?)$')

MAIL_SERVER_REGEX = re.compile(
    r'^mail-server:\/\/(?P<username>.*?):(?P<password>.*?)@(?P<server>.*?):(?P<port>.*?)/(?P<ssl>.*?)$')


def get_mysql_settings(url):
    matches = MYSQL_URL_REGEX.match(url)
    return {
        'username': matches.group('username'),
        'password': matches.group('password'),
        'host': matches.group('host'),
        'db_name': matches.group('db')
    }


def get_mail_server_config(url):
    matches = MAIL_SERVER_REGEX.match(url)
    return {
        'username': matches.group('username'),
        'password': matches.group('password'),
        'server': matches.group('server'),
        'port': matches.group('port'),
        'ssl': matches.group('ssl') == 'true'
    }


def generate_random_password():
    key = ''
    for i in range(16):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key


def get_reset_email_body(content):
    return f"Your password has been reset. " \
           f"Your new password is <b>{content}</b><br>Please change your password immediately. " \
           f"If you did not reset your password, contact Info-spectrum right now!"


def add_issue_email_body(content):
    return f"The following issue has been reported by {content.customer_name.data} on" \
           f" {str(content.issue_report_date.data)}. It is related to <b>{content.domain.data}</b> " \
           f"and is rated as <b>{content.priority.data}</b> priority.<br>" \
           f"<br>Please find the issue below:" \
           f"<br><b>{content.issue_description.data}</b><br>" \
           f"<br>Please look into the issue as soon as possible<br>" \
           f"<br>Thank You<br>"


def edit_issue_email_body(content, ticket):
    if content.status.data == 'Fixed':
        return f"The <b>Ticket# {ticket}</b> has been closed. Please inform the customer.<br>" \
               f"<br>Thank You<br>"
    else:
        return f"The following issue has been updated by {content.customer_name.data}. " \
               f"It is related to <b>{content.domain.data}</b> " \
               f"and is rated as <b>{content.priority.data}</b> priority.<br>" \
               f"<br>Please find the updated issue below:" \
               f"<br><b>{content.issue_description.data}</b><br>" \
               f"<br>Kindly speak to the customer in case you have any questions about it.<br>" \
               f"<br>Thank You<br>"


def get_reminder_email_content(ticket, user):
    return f"The user <b>{user}</b> is requesting an update on <b>Ticket# {ticket}</b>. " \
           f"<br>Please respond to the customer<br>" \
           f"<br>Thank You"


def get_recipients(recipient):
    recipient_list = ['suresh@info-spectrum.com']

    if recipient == 'Support':
        recipient_list.append('support@info-spectrum.com')
        recipient_list.append('amara@info-spectrum.com')
        recipient_list.append('ravi@info-spectrum.com')
        recipient_list.append('rbush@info-spectrum.com')
    elif recipient == 'Billing':
        recipient_list.append('billing@info-spectrum.com')
        recipient_list.append('srinivasan@info-spectrum.com')
    elif recipient == 'Development':
        recipient_list.append('sridhar@qwickbit.com')
        recipient_list.append('ravi@info-spectrum.com')
        recipient_list.append('rbush@info-spectrum.com')
        recipient_list.append('support@info-spectrum.com')
    else:
        recipient_list = [recipient]

    return recipient_list


def email_service(recipients, content, subject):
    mail = Mail()
    status = False

    try:
        msg = Message(subject,
                      sender="support@info-spectrum.com",
                      recipients=recipients)
        msg.html = content
        mail.send(msg)
        status = True
    except Exception as e:
        print(e)

    return status


def assign_customer_data_to_issue(db_issue, customer_data):
    db_issue.customer_name = customer_data.customer_name.data
    db_issue.company = customer_data.company.data
    db_issue.source = customer_data.source.data
    db_issue.email = customer_data.e_mail.data
    db_issue.phone = customer_data.phone_number.data
    db_issue.issue_report_date = customer_data.issue_report_date.data
    db_issue.issue_description = customer_data.issue_description.data
    db_issue.domain = customer_data.domain.data
    db_issue.priority = customer_data.priority.data
    db_issue.assigned_to = customer_data.assigned_to.data
    db_issue.support_engineer = customer_data.support_engineer.data
    db_issue.issue_fix_date = customer_data.issue_fixed_date.data
    db_issue.status = customer_data.status.data
    db_issue.support_engineer_comments = customer_data.support_engineer_comments.data
    return db_issue


def save_file_to_folder(folder_location, file, date_to_append_to_filename):
    name = secure_filename(file.filename)
    filename = date_to_append_to_filename + '-' + name
    file.save(os.path.join(folder_location, filename))
    return filename


def delete_old_file_from_folder(folder_location, filename):
    os.remove(os.path.join(folder_location, filename))
