
from passlib.context import CryptContext


def remove_uuid(response_json):
    del response_json["uuid"]
    return response_json


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = pwd_context.hash(password)
    print(password_hash)
