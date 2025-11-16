from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

def get_engine():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    connection_url = (
        f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )

    engine = create_engine(connection_url)
    return engine

