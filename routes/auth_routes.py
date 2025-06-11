from flask import Blueprint, request, jsonify
from db.connection import engine
from sqlalchemy import text
from auth.jwt_handler import create_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    with engine.begin() as conn:
        user = conn.execute(text("""
            SELECT UsuarioId FROM usuarios WHERE Usuario = :u AND Password = :p
        """), {"u": username, "p": password}).fetchone()

        if not user:
            return jsonify({"message": "Credenciales inválidas"}), 401

        token, expiration = create_token(username)


        # conn.execute(text("""
        #     INSERT INTO usuarios_token (username, token, expiration)
        #     VALUES (:u, :t, :e)
        # """), {"u": username, "t": token, "e": expiration})

        return jsonify({
            "Bearer": token,
            "ExpirationDate": expiration.isoformat()
        })
