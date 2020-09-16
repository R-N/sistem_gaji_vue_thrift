from db import DBEntity
from sqlalchemy import Column, Integer, String, Sequence, Boolean, orm
from utils.crypto import hash_bcrypt_sha256, verify_bcrypt_sha256
import validators.user as validator
from sqlalchemy.ext.hybrid import hybrid_property
import rpc.gen.akun.user.constants as user_constants

class DBUser(DBEntity):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(user_constants.USERNAME_LEN_MAX), unique=True, nullable=False)
    password = Column(String(77), nullable=False)
    name = Column(String(user_constants.NAME_LEN_MAX), nullable=False)
    email = Column(String(user_constants.EMAIL_LEN_MAX), unique=True, nullable=False)
    role = Column(Integer, nullable=False, default=0)
    enabled = Column(Boolean, default=True, nullable=False)
    refresh_secret_2 = Column(String(32), nullable=True, default=None)

    def __init__(
        self,
        username=None,
        password=None,
        role=None,
        name=None,
        email=None,
        enabled=None,
        my_role=None
    ):
        if role is not None:
            self.set_role(role, my_role=my_role)
        if username:
            self.set_username(username, my_role=my_role)
        if password:
            self.set_password(password, my_role=my_role)
        if name:
            self.set_name(name, my_role=my_role)
        if email:
            self.set_email(email, my_role=my_role)
        if enabled is not None:
            self.set_enabled(enabled, my_role=my_role)

    @orm.reconstructor
    def init_on_load(self):
        pass

    def __repr__(self):
        return "<User(id=%r, username=%r, name=%r, email=%r, role=%r, enabled=%r)>" % (self.id, self.username, self.name, self.email, self.role, self.enabled)

    def set_password(self, password, my_role=None):
        validator.validate_changer_role(self.role, my_role)
        validator.validate_password(password)
        self.password = hash_bcrypt_sha256(password)
        self.set_refresh_secret_2(None)

    def verify_password(self, password):
        return verify_bcrypt_sha256(self.password, password)

    def set_name(self, name, my_role=None):
        validator.validate_changer_role(self.role, my_role)
        validator.validate_name(name)
        self.name = name

    def set_role(self, role, my_role=None):
        validator.validate_changer_role(self.role, my_role)
        validator.validate_role(role, my_role=my_role)
        self.role = role
        self.set_refresh_secret_2(None)

    def set_username(self, username, my_role=None):
        validator.validate_changer_role(self.role, my_role)
        validator.validate_username(username)
        self.username = username

    def set_email(self, email, my_role=None):
        validator.validate_changer_role(self.role, my_role)
        validator.validate_email(email)
        self.email = email

    def set_enabled(self, enabled, my_role=None):
        validator.validate_changer_role(self.role, my_role)
        self.enabled = enabled
        self.set_refresh_secret_2(None)

    def set_refresh_secret_2(self, refresh_secret_2):
        self.refresh_secret_2 = refresh_secret_2
