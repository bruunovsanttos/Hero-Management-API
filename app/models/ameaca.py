from app.extensions import db
from .enums import NivelAmeaca, StatusAmeaca

class Ameaca(db.Model):
    __tablename__ = "ameaca"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.Enum(NivelAmeaca), nullable=False)
    status = db.Column(db.Enum(StatusAmeaca), nullable=False, default=StatusAmeaca.REGISTRADA)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self) -> str:
        return f"<Ameaca {self.titulo}>"
