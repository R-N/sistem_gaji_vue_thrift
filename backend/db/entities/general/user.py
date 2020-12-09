import re 

from .base import DbGeneralEntity
from sqlalchemy import Column, Integer, String, Sequence, Boolean, orm
from sqlalchemy.ext.hybrid import hybrid_property

from rpc.gen.user.user.types.ttypes import TUserRole
import rpc.gen.user.user.errors.constants as user_constants
from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode

from utils.crypto import hash_bcrypt_sha256, verify_bcrypt_sha256


class DbUser(DbGeneralEntity):
    # Columns

    __tablename__ = 'users'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    _username = Column("username", String(user_constants.USERNAME_LEN_MAX), unique=True, nullable=False)
    _password = Column("password", String(77), nullable=True, default=None)
    _name = Column("name", String(user_constants.NAME_LEN_MAX), nullable=False)
    _email = Column("email", String(user_constants.EMAIL_LEN_MAX), unique=True, nullable=False)
    _role = Column("role", Integer, nullable=False, default=TUserRole.ADMIN_BIASA)
    _verified = Column("verified", Boolean, nullable=False, default=False)
    _enabled = Column("enabled", Boolean, nullable=False, default=True)
    refresh_secret_2 = Column("refresh_secret_2", String(32), nullable=True, default=None)
    email_secret_2 = Column("email_secret_2", String(32), nullable=True, default=None)

    # Inits and stuff

    @orm.reconstructor
    def reconstruct(self):
        pass

    def __repr__(self):
        return "<User(id=%r, username=%r, name=%r, email=%r, role=%r, enabled=%r, confirmed=%r)>" % (self.id, self.username, self.name, self.email, self.role, self.enabled, self.confirmed)

    # Properties and other methods associated with columns

    # password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        DbUserValidator.validate_password(password)
        self.set_refresh_secret_2(None)
        self.set_email_secret_2(None)
        self._password = hash_bcrypt_sha256(password)

    @property
    def has_password(self):
        return self.verified and self.password

    def verify_password(self, password):
        return verify_bcrypt_sha256(self.password, password)

    def require_has_password(self, has_password):
        if has_password and not self.has_password:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        if not has_password and self.has_password:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)

    # name

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        DbUserValidator.validate_name(name)
        self._name = name

    # role

    @hybrid_property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        DbUserValidator.validate_role(role)
        self._role = role
        self.set_refresh_secret_2(None)

    # username

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        DbUserValidator.validate_username(username)
        self._username = username

    # email

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        DbUserValidator.validate_email(email)
        self.set_verified(False)
        self.set_email_secret_2(None)
        self._email = email

    # verified

    @hybrid_property
    def verified(self):
        return self._verified

    @verified.setter
    def verified(self, verified):
        if self.verified and verified:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
        self.set_email_secret_2(None)
        self.set_refresh_secret_2(None)
        self._verified = verified

    def require_verified(self, verified):
        if verified and not self.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        if not verified and self.verified:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)

    # enabled

    @hybrid_property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self.set_refresh_secret_2(None)
        self._enabled = enabled

    # Other methods

    def fill(self, obj):
        obj.id = self.id
        obj.username = self.username
        obj.role = self.role
        obj.name = self.name
        obj.email = self.email
        obj.enabled = self.enabled
        obj.verified = self.verified

        return obj

    # Validator

    def validator():
        return DbUserValidator


class DbUserValidator:
    EMAIL_REGEX = re.compile(user_constants.EMAIL_REGEX_STR)
    PASSWORD_REGEX = re.compile(user_constants.PASSWORD_REGEX_STR)
    USERNAME_REGEX = re.compile(user_constants.USERNAME_REGEX_STR)
    NAME_REGEX = re.compile(user_constants.NAME_REGEX_STR)

    def validate_role(role):
        if role is None:
            raise TUserError(TUserErrorCode.ROLE_EMPTY)
        if role not in TUserRole._VALUES_TO_NAMES:
            raise TUserError(TUserErrorCode.ROLE_INVALID)

    def validate_changer_role(changer_role, user_role):
        return (not user_role) or user_role != TUserRole.SUPER_ADMIN or changer_role == TUserRole.SUPER_ADMIN

    def validate_role_set(role, changer_role=None):
        DbUserValidator.validate_role(role)
        if role == TUserRole.SUPER_ADMIN and (changer_role != TUserRole.SUPER_ADMIN or not changer_role):
            raise TAuthError(TAuthErrorCode.ROLE_INVALID)

    def validate_email(email):
        if not email:
            raise TUserError(TUserErrorCode.EMAIL_EMPTY)
        if len(email) > user_constants.EMAIL_LEN_MAX:
            raise TUserError(TUserErrorCode.EMAIL_TOO_LONG)
        if not DbUserValidator.EMAIL_REGEX.match(email):
            raise TUserError(TUserErrorCode.EMAIL_INVALID)

    def validate_password(password):
        if not password:
            raise TUserError(TUserErrorCode.PASSWORD_EMPTY)
        if len(password) < user_constants.PASSWORD_LEN_MIN:
            raise TUserError(TUserErrorCode.PASSWORD_TOO_SHORT)
        if len(password) > user_constants.PASSWORD_LEN_MAX:
            raise TUserError(TUserErrorCode.PASSWORD_TOO_LONG)
        if not DbUserValidator.PASSWORD_REGEX.match(password):
            raise TUserError(TUserErrorCode.PASSWORD_INVALID)

    def validate_name(name):
        if not name:
            raise TUserError(TUserErrorCode.NAME_EMPTY)
        if len(name) > user_constants.NAME_LEN_MAX:
            raise TUserError(TUserErrorCode.NAME_TOO_LONG)
        if not DbUserValidator.NAME_REGEX.match(name):
            raise TUserError(TUserErrorCode.NAME_INVALID)

    def validate_username(username):
        if not username:
            raise TUserError(TUserErrorCode.USERNAME_EMPTY)
        if len(username) > user_constants.USERNAME_LEN_MAX:
            raise TUserError(TUserErrorCode.USERNAME_TOO_LONG)
        if not DbUserValidator.USERNAME_REGEX.match(username):
            raise TUserError(TUserErrorCode.USERNAME_INVALID)