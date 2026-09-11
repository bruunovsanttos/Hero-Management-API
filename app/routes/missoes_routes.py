from flask import Blueprint, request, jsonify
from app.services.missao_service import criar_missao, buscar_missao, listar_missoes, listar_missoes_por_status, listar_missoes_por_heroi, listar_missoes_por_ameaca, finalizar_missao, cancelar_missao


missao_bp = Blueprint("missoes", __name__)

@missao_bp.route("/missoes", methods=["POST"])
def criar():
    dados = request.get_json()

    heroi_id = dados.get("heroi_id")
    ameaca_id = dados.get("ameaca_id")

    missao, erro = criar_missao(heroi_id, ameaca_id)

    if erro:
        return jsonify({"erro": erro}), 404

    return jsonify({
        "id":missao.id,
        "heroi_id":missao.heroi_id,
        "ameaca_id":missao.ameaca_id,
        "status":missao.status.value
    }), 200

@missao_bp.route("/missoes/<int:missao_id>", methods=["GET"])
def buscar(missao_id):
    missao, erro = buscar_missao(missao_id)

    if erro:
        return jsonify({"erro": erro}), 404

    return jsonify({
        "id": missao.id,
        "heroi_id": missao.heroi_id,
        "ameaca_id": missao.ameaca_id,
        "status": missao.status.value
    }), 200

@missao_bp.route("/missoes", methods=["GET"])
def listar():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    missoes, erro = listar_missoes(page=page, per_page=per_page)

    if erro:
        return jsonify(({"erro": erro})), 400

    resultado = []

    for missao in missoes:
        resultado.append({
        "id": missao.id,
        "heroi_id": missao.heroi_id,
        "ameaca_id": missao.ameaca_id,
        "status": missao.status.value
    })

    return jsonify(resultado), 200

@missao_bp.route("/missoes/status/<status>", methods=["GET"])
def listar_por_status(status):
    missoes_por_status, erro = listar_missoes_por_status(status)

    if erro:
        return jsonify(({"erro": erro})), 400

    resultado = []

    for missao in missoes_por_status:
        resultado.append({
            "id": missao.id,
            "heroi_id": missao.heroi_id,
            "ameaca_id": missao.ameaca_id,
            "status": missao.status.value
        })

    return jsonify(missoes_por_status), 200

@missao_bp.route("/missoes/heroi/<int:heroi_id>", methods=["GET"])
def listar_por_heroi(heroi_id):
    missoes_por_heroi, erro = listar_missoes_por_heroi(heroi_id)

    if erro:
        return jsonify({"erro": erro}), 404

    resultado = []

    for missao in missoes_por_heroi:
        resultado.append({
            "id": missao.id,
            "heroi_id": missao.heroi_id,
            "ameaca_id": missao.ameaca_id,
            "status": missao.status.value
        })
    return jsonify(missoes_por_heroi), 200

@missao_bp.route("/missoes/ameaca/<int:ameaca_id>", methods=["GET"])
def listar_por_ameaca(ameaca_id):
    missoes_por_ameaca, erro = listar_missoes_por_ameaca(ameaca_id)

    if erro:
        return jsonify({"erro": erro}), 404

    resultado = []

    for missao in missoes_por_ameaca:
        resultado.append({
            "id": missao.id,
            "heroi_id": missao.heroi_id,
            "ameaca_id": missao.ameaca_id,
            "status": missao.status.value
        })
    return jsonify(missoes_por_ameaca), 200

@missao_bp.route("/missoes/<int:missao_id>/finalizar", methods=["PATCH"])
def finalizar(missao_id):

    missao, erro = finalizar_missao(missao_id)

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({
            "id": missao.id,
            "heroi_id": missao.heroi_id,
            "ameaca_id": missao.ameaca_id,
            "status": missao.status.value
        }), 200

@missao_bp.route("/missoes/<int:missao_id>/cancelar", methods=["PATCH"])
def cancelar(missao_id):

    missao, erro = cancelar_missao(missao_id)

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({
            "id": missao.id,
            "heroi_id": missao.heroi_id,
            "ameaca_id": missao.ameaca_id,
            "status": missao.status.value
        }), 200

