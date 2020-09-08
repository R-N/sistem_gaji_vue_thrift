from db import DBSession
from db.entities import DBUser
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS
class UserModel:
    def __init__(self):
        pass

    def get_user(self, username):
        with DBSession() as session:
            user = session.query(DBUser).filter(DBUser.username == username).first()
            return user
