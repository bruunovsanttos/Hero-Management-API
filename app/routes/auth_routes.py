from flask import Blueprint, request, jsonify
from app.services.auth_service import cadastrar_usuario, autenticar_usuario, buscar_usuario_autenticado
from flask_jwt_extended import jwt_required, get_jwt_identity

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

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict) or not dados:
        return jsonify({"erro": "informe dados do login em um objeto JSON"}), 400

    email = dados.get("email")
    senha = dados.get("senha")

    token, erro = autenticar_usuario(email, senha)

    if erro == "Email ou senha inválidos":
        return jsonify({"erro": erro}), 401

    if erro:
        return jsonify({"erro": erro}), 400

    return jsonify({"access_token": token}), 200

@auth_bp.route("/auth/me", methods=["GET"])
@jwt_required()
def usuario_atual():
    usuario_id = get_jwt_identity()

    usuario, erro= buscar_usuario_autenticado(usuario_id)

    if erro:
        return jsonify({"erro": erro}), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }), 200




