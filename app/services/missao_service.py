from app.models.heroi import Heroi
from app.models.missao import Missao
from app.models.ameaca import Ameaca
from app.models.enums import StatusHeroi, RankHeroi, NivelAmeaca, StatusAmeaca
from app.extensions import db

def criar_missao(heroi_id, ameaca_id):
    heroi = Heroi.query.get(heroi_id)
    ameaca = Ameaca.query.get(ameaca_id)


    if not heroi:
        return None, "Heroí não encontrado"

    if not ameaca:
        return None, "Ameaça não encontrada"

    if heroi.status != StatusHeroi.DISPONIVEL:
        return None, "Heroí não está disponível"

    ordem_rank = {
        RankHeroi.C: 1,
        RankHeroi.B: 2,
        RankHeroi.A: 3,
        RankHeroi.S: 4
    }

    ordem_ameaca = {
        NivelAmeaca.C: 1,
        NivelAmeaca.B: 2,
        NivelAmeaca.A: 3,
        NivelAmeaca.S: 4
    }

    if ordem_rank[heroi.rank] < ordem_ameaca[ameaca.nivel]:
        return None, "Heroí não possui rank suficiente para essa ameaça"

    missao = Missao(
        heroi_id = heroi_id,
        ameaca_id = ameaca_id
    )

    heroi.status = StatusHeroi.EM_MISSAO
    ameaca.status = StatusAmeaca.EM_ATENDIMENTO

    db.session.add(missao)
    db.session.commit()

    return missao, None