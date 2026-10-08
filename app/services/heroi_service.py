from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.heroi import Heroi
from app.models.enums import RankHeroi, StatusHeroi


def listar_herois():
    return Heroi.query.order_by(Heroi.id.asc()).all()


def criar_heroi(nome, codinome, rank, latitude, longitude):

    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome é obrigatório.")

    nome = nome.strip()
    if len(nome) > 120:
        raise ValueError("O nome deve ter no máximo 120 caracteres.")

    # Validar codinome
    if not isinstance(codinome, str) or not codinome.strip():
        raise ValueError("O codinome é obrigatório.")

    codinome = codinome.strip()

    if len(codinome) > 120:
        raise ValueError("O codinome deve ter no máximo 120 caracteres.")

    # Validar rank
    try:
        rank_enum = RankHeroi(rank)
    except (ValueError, TypeError):
        raise ValueError("Rank inválido. Utilize C, B, A ou S.")

    # Validar coordenadas
    try:
        latitude = Decimal(str(latitude))
        longitude = Decimal(str(longitude))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Latitude ou longitude inválida.")

    if not latitude.is_finite() or not longitude.is_finite():
        raise ValueError("As coordenadas devem ser números finitos.")

    if not -90 <= latitude <= 90:
        raise ValueError("Latitude deve estar entre -90 e 90.")

    if not -180 <= longitude <= 180:
        raise ValueError("Longitude deve estar entre -180 e 180.")

    # Verificar duplicidade
    heroi_existente = Heroi.query.filter_by(
        codinome=codinome
    ).first()

    if heroi_existente:
        raise ValueError("Já existe um herói com esse codinome.")

    if Heroi.query.filter_by(nome=nome).first():
        raise ValueError("Já existe um herói com esse nome.")

    # Criar herói
    novo_heroi = Heroi(
        nome=nome,
        codinome=codinome,
        rank=rank_enum,
        status=StatusHeroi.DISPONIVEL,
        latitude=latitude,
        longitude=longitude
    )

    try:
        db.session.add(novo_heroi)
        db.session.commit()

    except IntegrityError as erro:
        db.session.rollback()
        # Identificar violações UNIQUE em SQLite e PostgreSQL, inclusive
        # quando outro cadastro é confirmado após a consulta inicial.
        original = erro.orig
        duplicidade = (
            getattr(original, "sqlite_errorname", None) == "SQLITE_CONSTRAINT_UNIQUE"
            or getattr(original, "sqlstate", None) == "23505"
        )
        if duplicidade:
            if Heroi.query.filter_by(codinome=codinome).first():
                raise ValueError("Já existe um herói com esse codinome.") from erro
            if Heroi.query.filter_by(nome=nome).first():
                raise ValueError("Já existe um herói com esse nome.") from erro
        raise

    except Exception:
        db.session.rollback()
        raise

    return novo_heroi