## Setup venv

- Open terminal in the current folder
- Run `python -m venv .venv`
- To install packages, run `pip install -r requirements.txt`
- Create `.env` file in `rag_backend` folder

## To set up the database

- Use sudo apt-install postgresql-16-pgvector
- Go to the psql shell and database.
- Run the SQL statement `CREATE EXTENSION IF NOT EXISTS VECTOR`.

## Add a dummy user 

- Go to the rag_backend folder
- Run the following shell script to create a new user to get the password
- """
    from app.models import User
    from app.database import SessionLocal

    db = SessionLocal()
    hashed_password = User.hash_password("your_password")
    new_user = User(username="your_username", hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.close()
  """

## Running the server

- Go to the rag_backend folder
- Run the command `uvicorn main:app --reload --host 0.0.0.0`

## Running the docker file

- Go to the rag_backend folder
- Run the command docker-compose up --build 


