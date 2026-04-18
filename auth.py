import jwt
import datetime

SECRET = "your_secret_key"

def create_token(username):
    return jwt.encode({
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET, algorithm="HS256")


def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None