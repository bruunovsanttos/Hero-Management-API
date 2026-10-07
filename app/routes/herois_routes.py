from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.heroi_service import listar_herois


herois_bp = Blueprint("herois", __name__)


@herois_bp.route("/herois", methods=["GET"])
@jwt_required()
def listar():
    herois = listar_herois()

    resultado = []

    for heroi in herois:
        resultado.append({
            "id": heroi.id,
            "codinome": heroi.codinome,
            "rank": heroi.rank.value,
            "status": heroi.status.value,
            "latitude": float(heroi.latitude),
            "longitude": float(heroi.longitude),
        })

    return jsonify(resultado), 200