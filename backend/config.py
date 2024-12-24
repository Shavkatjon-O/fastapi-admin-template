import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

POSTGRESQL_DB_URI = os.environ.get("POSTGRESQL_DB_URI")

# authentication
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
