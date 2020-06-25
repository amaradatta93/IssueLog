import os

username = os.getenv('MYSQL_DATABASE_USER')
password = os.getenv('MYSQL_DATABASE_PASSWORD')
host = os.getenv('MYSQL_DATABASE_HOST')
db_name = os.getenv('MYSQL_DATABASE_DB')
UPLOAD_FOLDER = os.path.abspath(os.curdir) + '/upload_folder/'
