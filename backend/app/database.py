import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


load_dotenv()


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME"),
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def test_database_connection():
    """Testa a conexão com o PostgreSQL."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Conexão com PostgreSQL realizada com sucesso!")

        return True

    except Exception as error:
        print(f"Erro ao conectar ao PostgreSQL: {error}")

        return False


if __name__ == "__main__":
    test_database_connection()