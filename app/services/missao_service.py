from app.models.heroi import Heroi
from app.models.missao import Missao
from app.models.ameaca import Ameaca
from app.models.enums import StatusHeroi, RankHeroi, NivelAmeaca, StatusAmeaca, StatusMissao
from app.extensions import db

def criar_missao(heroi_id, ameaca_id):
    heroi = Heroi.query.get(heroi_id)
    ameaca = Ameaca.query.get(ameaca_id)


    if not heroi:
        return None, "Herói não encontrado"

    if not ameaca:
        return None, "Ameaça não encontrada"

    if heroi.status != StatusHeroi.DISPONIVEL:
        return None, "Herói não está disponível"
    
    if ameaca.status != StatusAmeaca.REGISTRADA:
        return None, "Ameaça não está disponível para atendimento"

    

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
        return None, "Herói não possui rank suficiente para essa ameaça"

    missao = Missao(
        heroi_id = heroi_id,
        ameaca_id = ameaca_id
    )

    heroi.status = StatusHeroi.EM_MISSAO
    ameaca.status = StatusAmeaca.EM_ATENDIMENTO

    db.session.add(missao)
    db.session.commit()

    return missao, None

def finalizar_missao(missao_id):
    missao = Missao.query.get(missao_id)

    if not missao:
        return None, "Missão não encontrada"

    if missao.status != StatusMissao.EM_ANDAMENTO:
        return None, "Missão não está em andamento"

    missao.status = StatusMissao.CONCLUIDA
    missao.finalizada_em = db.func.now()

    missao.heroi.status = StatusHeroi.DISPONIVEL
    missao.ameaca.status = StatusAmeaca.RESOLVIDA

    db.session.commit()

    return missao, None


def cancelar_missao(missao_id):
    missao = Missao.query.get(missao_id)

    if not missao:
        return None, "Missão não encontrada"

    if missao.status != StatusMissao.EM_ANDAMENTO:
        return None, "Missão não está em andamento"

    missao.status = StatusMissao.CANCELADA
    missao.finalizada_em = db.func.now()

    missao.heroi.status = StatusHeroi.DISPONIVEL
    missao.ameaca.status = StatusAmeaca.REGISTRADA

    db.session.commit()

    return missao, None