from db import DBEntity
from sqlalchemy import Column, Integer, String, Sequence
from utils.crypto import hash_bcrypt_sha256, verify_bcrypt_sha256

class DBUser(DBEntity):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(77))
    name = Column(String(50))
    email = Column(String(50))
    role = Column(Integer)

    def __repr__(self):
        return "<User(id=%r, username=%r, name=%r, email=%r, role=%r)>" % (self.id, self.username, self.name, self.email, self.role)

    def set_password(self, password):
        self.password = hash_bcrypt_sha256(password)

    def verify_password(self, password):
        return verify_bcrypt_sha256(self.password, password)