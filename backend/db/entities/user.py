from db import DBEntity
from sqlalchemy import Column, Integer, String, Sequence, Boolean, orm
from utils.crypto import hash_bcrypt_sha256, verify_bcrypt_sha256
import validators.user as validator
from sqlalchemy.ext.hybrid import hybrid_property
import rpc.gen.akun.user.constants as user_constants

class DBUser(DBEntity):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(user_constants.USERNAME_LEN_MAX), unique=True)
    password = Column(String(77))
    name = Column(String(user_constants.NAME_LEN_MAX))
    email = Column(String(user_constants.EMAIL_LEN_MAX), unique=True)
    role = Column(Integer)
    enabled = Column(Boolean, default=True)
    refresh_secret_2 = Column(String(32), nullable=True, default=None)

    def __init__(
        self,
        username=None,
        password=None,
        role=None,
        name=None,
        email=None,
        enabled=None,
        session=None,
        my_role=None
    ):
        if username:
            self.set_username(username, session=session)
        if password:
            self.set_password(password)
        if name:
            self.set_name(name)
        if email:
            self.set_email(email, session=session)
        if role is not None:
            self.set_role(role, my_role=my_role)
        if enabled is not None:
            self.set_enabled(enabled)

    @orm.reconstructor
    def init_on_load(self):
        pass

    def __repr__(self):
        return "<User(id=%r, username=%r, name=%r, email=%r, role=%r, enabled=%r)>" % (self.id, self.username, self.name, self.email, self.role, self.enabled)

    def set_password(self, password):
        validator.validate_password(password)
        self.password = hash_bcrypt_sha256(password)
        self.set_refresh_secret_2(None)

    def verify_password(self, password):
        return verify_bcrypt_sha256(self.password, password)

    def set_name(self, name):
        validator.validate_name(name)
        self.name = name

    def set_role(self, role, my_role=None):
        validator.validate_role(role, my_role=my_role)
        self.role = role
        self.set_refresh_secret_2(None)

    def set_username(self, username, session=None):
        validator.validate_username(username, session=session)
        self.username = username

    def set_email(self, email, session=None):
        validator.validate_email(email, session=session)
        self.email = email

    def set_enabled(self, enabled):
        self.enabled = enabled

    def set_refresh_secret_2(self, refresh_secret_2):
        self.refresh_secret_2 = refresh_secret_2
