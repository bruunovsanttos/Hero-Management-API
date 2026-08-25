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

    missao_ativa_heroi = Missao.query.filter_by(heroi_id=heroi_id, status=StatusMissao.EM_ANDAMENTO).first()

    if missao_ativa_heroi:
        return None, "Herói já possui uma missão em andamento"

    missao_ativa_ameaca = Missao.query.filter_by(ameaca_id=ameaca_id, status=StatusMissao.EM_ANDAMENTO).first()

    if missao_ativa_ameaca:
        return None, "Ameaça já possui uma missão em andamento"


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
        ameaca_id = ameaca_id, status=StatusMissao.EM_ANDAMENTO
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


def buscar_missao(missao_id):
    missao = Missao.query.get(missao_id)

    if not missao:
        return None, "Missão não encontrada"

    return missao, None


def listar_missoes():
    missoes = Missao.query.all()

    return missoes, None


def listar_misoes_em_andamento():
    missoes = Missao.query.filter_by(status=StatusMissao.EM_ANDAMENTO).all()

    return missoes, None

def listar_missoes_por_status(status):
    status_validos = [StatusMissao.EM_ANDAMENTO.value, StatusMissao.CONCLUIDA.value, StatusMissao.CANCELADA.value]

    if status not in status_validos:
        return None, "Status de missão inválido"

    status_missao = StatusMissao(status)

    missoes = Missao.query.filter_by(status=status_missao).all()

    return missoes, None


def listar_missoes_por_heroi(heroi_id):
    heroi = Heroi.query.get(heroi_id)

    if not heroi:
        return None, "Herói não encontrado"

    missoes = Missao.query.filter_by(heroi_id=heroi_id).all()

    return missoes, None