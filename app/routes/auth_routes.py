from flask import Blueprint, request, jsonify
from app.services.auth_service import cadastrar_usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/cadastro", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)


    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "informe os dados do cadastro em um objeto JSON"}), 400

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    usuario, erro = cadastrar_usuario(nome, email, senha)

    if erro == "Email já cadastrado":
        return jsonify({"erro": erro}), 409

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }), 201
