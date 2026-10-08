from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.heroi_service import listar_herois, criar_heroi


herois_bp = Blueprint("herois", __name__)


@herois_bp.route("/herois", methods=["GET"])
@jwt_required()
def listar():
    herois = listar_herois()

    resultado = []

    for heroi in herois:
        resultado.append({
            "id": heroi.id,
            "nome": heroi.nome,
            "codinome": heroi.codinome,
            "rank": heroi.rank.value,
            "status": heroi.status.value,
            "latitude": float(heroi.latitude),
            "longitude": float(heroi.longitude),
        })

    return jsonify(resultado), 200


@herois_bp.route("/herois", methods=["POST"])
@jwt_required()
def criar():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON válido."}), 400

    campos_obrigatorios = [
        "nome",
        "codinome",
        "rank",
        "latitude",
        "longitude",
    ]

    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            return jsonify({
                "erro": f"Campo obrigatório: {campo}"
            }), 400

    try:
        heroi = criar_heroi(
            nome=dados["nome"],
            codinome=dados["codinome"],
            rank=dados["rank"],
            latitude=dados["latitude"],
            longitude=dados["longitude"],
        )

        return jsonify({
            "id": heroi.id,
            "nome": heroi.nome,
            "codinome": heroi.codinome,
            "rank": heroi.rank.value,
            "status": heroi.status.value,
            "latitude": float(heroi.latitude),
            "longitude": float(heroi.longitude),
        }), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400