from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.email.errors.ttypes import TUserEmailError, TUserEmailErrorCode
from rpc.gen.user.management.errors.ttypes import TUserManagementError, TUserManagementErrorCode

from .crud import CrudModel

import db
from db.entities.general import DbUser
from db.errors import UniqueError

load_dotenv()

# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS


class UserModel(CrudModel):
    def __init__(self):
        CrudModel.__init__(
            self, 
            DbUser, 
            TUserError, 
            TUserErrorCode, 
            name_field="name", 
            actions={
                "get": TUserRole.ADMIN_AKUN,
                "create": TUserRole.ADMIN_AKUN,
                "fetch": TUserRole.ADMIN_AKUN,
                "delete": TUserRole.ADMIN_AKUN,
            },
            setters={
                "name": TUserRole.ADMIN_AKUN,
                "role": TUserRole.ADMIN_AKUN,
                "email": TUserRole.SUPER_ADMIN,
                "password": TUserRole.SUPER_ADMIN,
                "enabled": TUserRole.ADMIN_AKUN,
                "verified": TUserRole.SUPER_ADMIN,
            },
        )

    def parse_error(self, parsed):
        if isinstance(parsed, UniqueError):
            if parsed.column == "email":
                raise TUserError(TUserErrorCode.EMAIL_ALREADY_EXISTS)
            if parsed.column == "username":
                raise TUserError(TUserErrorCode.USERNAME_ALREADY_EXISTS)

    def get_by_username_email_silent(self, username):
        return db.session.query(DbUser).filter(
            (DbUser.username == username) | (DbUser.email == username)
        ).scalar()

    def get_by_username_email(self, username):
        user = self.get_by_username_email_silent(username)
        if not user:
            raise TUserError(TUserErrorCode.USER_NOT_FOUND)
        return user

    def fetch(self, query=None, actor=None):
        db_query = CrudModel.fetch(self, query, actor=actor, execute=False)
        return db_query.all()

    def set_email(self, user, value, actor=None):
        if user.verified:
            try:
                self.validate_actor_role(actor, TUserRole.SUPER_ADMIN)
            except (TAuthError, TUserError):
                raise TUserError(TUserErrorCode.ALREADY_VERIFIED)
        CrudModel.set_field(self, user, value, actor=actor, required_role=TUserRole.SUPER_ADMIN)
        db.session.add(user)

    def verify_email(self, user, email_secret_2, email, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        if user.has_password:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)

        self.set_password(user, password, actor=TUserRole.SUPER_ADMIN)
        self.set_email(user, email, actor=TUserRole.SUPER_ADMIN)
        user.verified = True
        db.session.add(user)

    def change_email(self, user, email_secret_2, email, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        if not user.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        if not user.verify_password(password):
            raise TAuthError(TAuthErrorCode.PASSWORD_SALAH)

        self.set_email(user, email, actor=TUserRole.SUPER_ADMIN)
        user.verified = True
        db.session.add(user)

    def reset_password(self, user, email_secret_2, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED)
        if not user.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)

        self.set_password(user, password, actor=TUserRole.SUPER_ADMIN)
