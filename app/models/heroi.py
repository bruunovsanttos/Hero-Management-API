from app.extensions import db
from .enums import RankHeroi, StatusHeroi
class Heroi(db.Model):
    __tablename__ = "heroi"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False, unique=True)
    codinome = db.Column(db.String(120),nullable=False, unique=True)
    rank = db.Column(db.Enum(RankHeroi), nullable=False)
    status = db.Column(db.Enum(StatusHeroi), nullable=False, default=StatusHeroi.DISPONIVEL)
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    missoes= db.relationship("Missao", back_populates="heroi")


    def __repr__(self) -> str:
        return f"<Heroi {self.codinome}>"
