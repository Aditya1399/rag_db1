To run the code, first enable the virtual environment using 
1. python3 -m venv <env_name>
2. source <env_name>/bin/activate

Install the necessary libraries, present in the requirements file.

Run the following commands,
1. sudo apt-install postgresql-16-pgvector

and then inside the psql shell run the command 
'CREATE EXTENSION IF NOT EXISTS VECTOR'

To run the migrations, first install alembic using sudo apt install alembic
alembic revision --autogenerate -m "Command Name"


