import re 

from .base import DbGeneralEntity
from sqlalchemy import Column, Integer, String, Sequence, Boolean, orm
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from rpc.gen.user.user.types.ttypes import TUserRole
import rpc.gen.user.user.types.ttypes as user_types
import rpc.gen.user.user.errors.constants as user_constants
from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.user.errors.constants import T_USER_ERROR_STR
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode
from rpc.gen.user.management.errors.ttypes import TUserManagementError, TUserManagementErrorCode
from rpc.gen.user.user.types.constants import T_ROLE_DOUBLES
from ...validator import bind_rules, create_rules_fields

from utils.crypto import hash_bcrypt_sha256, verify_bcrypt_sha256
import traceback
class DbUser(DbGeneralEntity):
    # Columns

    __tablename__ = 'users'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(user_constants.USERNAME_MAX_LEN), unique=True, nullable=False)
    password = Column("password", String(83), nullable=True, default=None)
    name = Column("name", String(user_constants.NAME_MAX_LEN), nullable=False)
    email = Column("email", String(user_constants.EMAIL_MAX_LEN), unique=True, nullable=False)
    role = Column("role", Integer, nullable=False, default=TUserRole.ADMIN_BIASA)
    verified = Column("verified", Boolean, nullable=False, default=False)
    enabled = Column("enabled", Boolean, nullable=False, default=True)
    refresh_secret_2 = Column("refresh_secret_2", String(32), nullable=True, default=None)
    email_secret_2 = Column("email_secret_2", String(32), nullable=True, default=None)

    # Inits and stuff

    @orm.reconstructor
    def reconstruct(self):
        pass

    def __repr__(self):
        return "<User(id=%r, username=%r, name=%r, email=%r, role=%r, enabled=%r, verified=%r)>" % (self.id, self.username, self.name, self.email, self.role, self.enabled, self.verified)

    # Properties and other methods associated with columns

    # password
    @validates("password")
    def validate_password(self, key, password):
        DbUserValidator.validate_password(password)
        self.refresh_secret_2 = None
        self.email_secret_2 = None
        return hash_bcrypt_sha256(password)

    @property
    def has_password(self):
        return self.verified and self.password

    def verify_password(self, password):
        return verify_bcrypt_sha256(self.password, password)

    def require_has_password(self, has_password):
        if has_password and not self.has_password:
            raise TUserError(TUserErrorCode.UNVERIFIED)
        if not has_password and self.has_password:
            raise TUserError(TUserErrorCode.ALREADY_VERIFIED)

    # others

    @validates("name")
    def validate_name(self, key, name):
        DbUserValidator.validate_name(name)
        return name

    @validates("role")
    def validate_role(self, key, role):
        DbUserValidator.validate_role(role)
        self.refresh_secret_2 = None
        return role

    @validates("username")
    def validate_username(self, key, username):
        DbUserValidator.validate_username(username)
        return username

    @validates("email")
    def validate_email(self, key, email):
        # if self.verified:
        #     raise TUserError(TUserErrorCode.ALREADY_VERIFIED)
        DbUserValidator.validate_email(email)
        self.verified = False
        self.email_secret_2 = None
        return email

    @validates("enabled")
    def validate_enabled(self, key, enabled):
        self.refresh_secret_2 = None
        self._enabled = enabled
        return enabled

    @validates("verified")
    def validate_verified(self, key, verified):
        if self.verified and verified:
            raise TUserError(TUserErrorCode.ALREADY_VERIFIED)
        if verified and not self.password:
            #traceback.print_stack()
            raise TUserManagementError(TUserManagementErrorCode.PASSWORD_EMPTY)
        self.email_secret_2 = None
        self.refresh_secret_2 = None
        self._verified = verified
        return verified

    def require_verified(self, verified):
        if verified and not self.verified:
            raise TUserError(TUserErrorCode.UNVERIFIED)
        if not verified and self.verified:
            raise TUserError(TUserErrorCode.ALREADY_VERIFIED)

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
    def validate_actor_role(actor_role, roles, Exception=TAuthError, error_code=TAuthErrorCode.ROLE_INVALID):
        if hasattr(actor_role, "role"):
            actor_role = actor_role.role
        if hasattr(actor_role, "__getitem__") and "role" in actor_role:
            actor_role = actor_role["role"]
        if not hasattr(roles, "__iter__"):
            roles = [roles]
        allowed_roles = {j for i in roles for j in T_ROLE_DOUBLES[i]}
        if actor_role not in allowed_roles:
            traceback.print_stack()
            if Exception:
                raise Exception(error_code)
            return False
        return True

bind_rules(DbUserValidator, create_rules_fields(
    TUserError,
	["USERNAME", "NAME", "PASSWORD", "EMAIL", "ROLE"],
	user_constants,
	user_types, 
	TUserErrorCode, 
	T_USER_ERROR_STR, 
	"USER"
))
