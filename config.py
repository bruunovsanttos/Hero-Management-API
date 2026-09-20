import os

from dotenv import load_dotenv

load_dotenv()


def get_required_env(nome):
    valor = os.getenv(nome)

    if not valor:
        raise RuntimeError(
            f"Variável de ambiente obrigatória não configurada: {nome}"
        )

    return valor


database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///hero_management.db",
)

if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )


class Config:
    SECRET_KEY = get_required_env("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = get_required_env("JWT_SECRET_KEY")