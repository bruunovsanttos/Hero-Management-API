from flask import Blueprint, request, jsonify
from app.services.missao_service import criar_missao, buscar_missao


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

