import os

from server.utils import get_mysql_settings, get_mail_server_config

# MySQL connection
mysql_config = get_mysql_settings(os.getenv('MYSQL_DATABASE_URL'))
username = mysql_config['username']
password = mysql_config['password']
host = mysql_config['host']
db_name = mysql_config['db_name']

# Info-spectrum email service
mail_server_config = get_mail_server_config(os.getenv('MAIL_SERVER_CONFIG'))
mail_username = mail_server_config['username']
mail_password = mail_server_config['password']
mail_server = mail_server_config['server']
mail_port = mail_server_config['port']
mail_use_ssl = mail_server_config['ssl']

# File upload folder
UPLOAD_FOLDER = os.path.abspath(os.curdir) + '/upload_folder/'
