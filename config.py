import os
#
# from flask import Flask
#
# app = Flask(__name__)

# MySQL configurations
username = os.getenv('MYSQL_DATABASE_USER')
password = os.getenv('MYSQL_DATABASE_PASSWORD')
host = os.getenv('MYSQL_DATABASE_HOST')
db_name = os.getenv('MYSQL_DATABASE_DB')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{host}/{db_name}'
