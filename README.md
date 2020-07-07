This web application uses python 3.6.9 and is built to handle the Infospectrum Issue Log.

#Clone the repository

#Client:
Open terminal and navigate into infoTRAK directory. 
Build the angular app: `npm install` Serve app : `sudo ng serve`

#Server: 
Create a virtual environment using: `python3 -m venv env`. 
Activate virtual env: `source env/bin/activate`. 
Install requirements: `pip install -r requirements.txt`. 
Install project: `pip install -e .`
Set the flask app: `export FLASK_APP=server`. 
Set the app configuration: `export FLASK_DEV=development`. 

#Database Configuration
Set the MYSQL_DATABASE_URL environment variable in the format: `mysql://username:password@host/dbname`. 
Migrate and upgrade the database: `flask db init` `flask db stamp head` `flask db migrate` `flask db upgrade`

#E-Mail server configuration
Set the MAIL_SERVER_CONFIG environment variable in the format: 
`mail-server://username:password@smtp_server:smtp_port/mail_use_ssl`

# Run the project
`flask run`
Browse to http://localhost:5000/
