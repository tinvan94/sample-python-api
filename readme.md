Build setup

Make sure you have Python3.x installed on your system.

We'll use PostgreSQL database for this tutorial. Install Postgres database if you don't have it installed already.

Make sure virtualenv is installed on your system.

Create your database and config correctly username, password and database_name

Make sure you change the above settings with the appropriate values
for your configuration. Change the username and password to your
correct database credentials


Running migrations

    python migrate.py db init

    python migrate.py db migrate

    python migrate.py db upgrade

From your terminal, make sure you are on the root folder of the app then run this command:
    
    python run.py

Enpoint Collects

get all customers
    GET - http://127.0.0.1:5000/api/customer

get customer by id
    GET - http://127.0.0.1:5000/api/customer/id

create a new customer
    POST - http://127.0.0.1:5000/api/customer

update info customer
    PUT - http://127.0.0.1:5000/api/customer

delete customer
    DELETE - http://127.0.0.1:5000/api/customer
