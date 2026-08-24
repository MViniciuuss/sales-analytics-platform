from getpass import getpass

from pwdlib import PasswordHash
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from backend.app.database import engine


password_manager = PasswordHash.recommended()


def create_users_table():
    query = text(
        """
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            full_name VARCHAR(120) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(query)

    print("Tabela users pronta!")


def create_user():
    full_name = input("Nome do usuário: ").strip()
    email = input("E-mail: ").strip().lower()

    password = getpass("Senha: ")
    password_confirmation = getpass("Repita a senha: ")

    if password != password_confirmation:
        print("As senhas não são iguais.")
        return

    if len(password) < 8:
        print("A senha precisa ter pelo menos 8 caracteres.")
        return

    hashed_password = password_manager.hash(password)

    query = text(
        """
        INSERT INTO users (
            full_name,
            email,
            password_hash
        )
        VALUES (
            :full_name,
            :email,
            :password_hash
        )
        """
    )

    try:
        with engine.begin() as connection:
            connection.execute(
                query,
                {
                    "full_name": full_name,
                    "email": email,
                    "password_hash": hashed_password,
                },
            )

        print("Usuário criado com sucesso!")

    except IntegrityError:
        print("Já existe um usuário com esse e-mail.")


def main():
    create_users_table()
    create_user()


if __name__ == "__main__":
    main()