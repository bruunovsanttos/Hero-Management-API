from app.extensions import db
from app.models.usuario import Usuario
from flask_jwt_extended import create_access_token

def cadastrar_usuario(nome, email, senha):
    if not isinstance(nome, str):
        return None, "Nome deve ser um texto"

    if not isinstance(email, str):
        return None, "Email deve ser um texto"

    if not isinstance(senha, str):
        return None, "Senha deve ser um texto"

    nome = nome.strip()
    email = email.strip().lower()
    
    if not nome or not email or not senha.strip():
        return None, "Nome, email e senha são obrigatórios"

    if len(nome) > 120:
        return None, "Nome deve ter no máximo 120 caracteres"

    if len(email) > 255:
        return None, "Email deve ter no máximo 255 caracteres"

    if email.count("@") != 1:
        return None, "Email inválido"

    parte_local, dominio = email.split("@")

    if not parte_local or not dominio:
        return None, "Email inválido"

    for caractere in email:
        if caractere.isspace():
            return None, "Email inválido"

    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        return None, "Email já cadastrado"

    usuario = Usuario(nome=nome, email=email)
    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    return usuario, None


def autenticar_usuario(email, senha):
    if not isinstance(email, str):
        return None, "Email deve ser um texto"

    if not isinstance(senha, str):
        return None, "Senha deve ser um texto"

    email = email.strip().lower()

    if not email or not senha.strip():
        return None, "Email e senha são obrigatórios"

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return None, "Email ou senha inválidos"

    if not usuario.verificar_senha(senha):
        return None, "Email ou senha inválidos"

    token = create_access_token(identity=str(usuario.id))

    return token, None

def buscar_usuario_autenticado(usuario_id):
    usuario = Usuario.query.filter_by(id=usuario_id).first()

    if not usuario:
        return None, "Usuário não encontrado"

    return usuario, None

