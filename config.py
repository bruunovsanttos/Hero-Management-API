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


class Config:
    SECRET_KEY = get_required_env("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///hero_management.db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = get_required_env("JWT_SECRET_KEY")