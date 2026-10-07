from app.models.heroi import Heroi


def listar_herois():
    return Heroi.query.order_by(Heroi.id.asc()).all()