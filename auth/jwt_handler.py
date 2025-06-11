import jwt, datetime
from config import SECRET_KEY

def create_token(username):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': expiration}, SECRET_KEY, algorithm='HS256')
    return token, expiration

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
