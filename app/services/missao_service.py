from app.models.heroi import Heroi
from app.models.missao import Missao

def criar_missao(heroi_id, ameaca_id):
    heroi = Heroi.query.get(heroi_id)

    if not heroi:
        return None, "Heroí não encontrado"

    if heroi.status != "Disponível":
        return None, "Heroí não está disponível"

    missao = Missao(
        heroi_id = heroi_id,
        ameaca_id = ameaca_id
    )

    return missao, None