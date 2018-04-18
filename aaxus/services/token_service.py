from itsdangerous import URLSafeTimedSerializer
from aaxus import app

app.config.from_pyfile('config.py')

def generate_confirmation_token(name):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(name, salt = app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        name = serializer.loads(
            token,
            salt = app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return name