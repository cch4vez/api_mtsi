from flask import request, jsonify
from functools import wraps
from auth.jwt_handler import decode_token
from db.connection import engine
from sqlalchemy import text
from datetime import datetime

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace("Bearer ", "")
        if not token:
            return jsonify({'message': 'Token requerido'}), 403
        try:
            data = decode_token(token)
            username = data['username']
        except Exception as e:
            return jsonify({'message': f'Token inválido: {str(e)}'}), 403

        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 1 FROM usuarios_token 
                WHERE username = :u AND token = :t AND expiration > :now
            """), {"u": username, "t": token, "now": datetime.utcnow()}).fetchone()

            if not result:
                return jsonify({'message': 'Token expirado o no válido'}), 403

        return f(username, *args, **kwargs)
    return wrapper
