from app.extensions import db
from .enums import StatusMissao

class Missao(db.Model):
    __tablename__ = "missao"

    id = db.Column(db.Integer, primary_key=True)
    heroi_id = db.Column(db.Integer, db.ForeignKey("heroi.id"), nullable =False)
    ameaca_id = db.Column(db.Integer, db.ForeignKey("ameaca.id"), nullable=False)
    status = db.Column(db.Enum(StatusMissao), nullable=False, default=StatusMissao.EM_ANDAMENTO)
    iniciada_em = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    finalizada_em = db.Column(db.DateTime, nullable=True)

    #isso representa a relacação das tabelas e deve ser colcoado em todas as tabelas que tem relações
    #se não ele não consegue ler e pode dar erro
    heroi = db.relationship("Heroi", back_populates="missoes")
    ameaca = db.relationship("Ameaca", back_populates="missoes")

    def __repr__(self) -> str:
        return f"<Missao {self.id}>"


