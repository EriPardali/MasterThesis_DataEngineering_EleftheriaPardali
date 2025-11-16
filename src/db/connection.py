from sqlalchemy import create_engine

def get_engine():
    db_user = "postgres"
    db_pass = "postgres"
    db_host = "localhost"
    db_port = "5432"
    db_name = "loan_portfolio_db"

    connection_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_url)
    return engine

