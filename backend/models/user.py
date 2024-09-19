from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.email.errors.ttypes import TUserEmailError, TUserEmailErrorCode
from rpc.gen.user.management.errors.ttypes import TUserManagementError, TUserManagementErrorCode

import db
from db.entities.general import DbUser
from db.errors import UniqueError

load_dotenv()

# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS


class UserModel:
    def __init__(self):
        pass

    def parse_error(self, parsed):
        if isinstance(parsed, UniqueError):
            if parsed.column == "email":
                raise TUserError(TUserErrorCode.EMAIL_ALREADY_EXISTS)
            if parsed.column == "username":
                raise TUserError(TUserErrorCode.USERNAME_ALREADY_EXISTS)

    def commit(self):
        try:
            db.commit()
        except IntegrityError as ex:
            self.parse_error(ex)
            raise

    def get_by_id(self, user_id):
        user = db.session.query(DbUser).filter(DbUser.id == user_id).scalar()
        if not user:
            raise TUserError(TUserErrorCode.USER_NOT_FOUND)
        return user

    def get_by_username_email_silent(self, username):
        return db.session.query(DbUser).filter(
            (DbUser.username == username) | (DbUser.email == username)
        ).scalar()

    def get_by_username_email(self, username):
        user = self._get_user_by_username_email(username)
        if not user:
            raise TUserError(TUserErrorCode.USER_NOT_FOUND)
        return user

    def fetch(self, query=None):
        db_query = db.session.query(DbUser)
        db_query = db_query.order_by(DbUser.enabled.desc(), DbUser.verified.desc(), DbUser.name.asc())
        if query:
            if query.enabled is not None:
                db_query = db_query.filter(DbUser.enabled == query.enabled)
            if query.verified is not None:
                db_query = db_query.filter(DbUser.verified == query.verified)
            if query.role is not None:
                DbUser.validator().validate_role(query.role)
                db_query = db_query.filter(DbUser.role == query.role)
            if query.limit:
                offset = query.offset if query.offset else 0
                db_query = db_query[offset:query.limit + offset]
        return db_query.all()

    def set_role(self, changer_role, user, role):
        self.validate_changer_role(changer_role, user.role)
        self.validate_role_set(role, changer_role)
        user.role = role
        db.session.add(user)

    def set_email(self, changer_role, user, email):
        if user.verified and changer_role != TUserRole.SUPER_ADMIN:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
        self.validate_changer_role(changer_role, user.role)
        user.email = email
        db.session.add(user)

    def set_password(self, changer_role, user, password):
        self.validate_changer_role(changer_role, user.role)
        user.password = password
        db.session.add(user)

    def set_enabled(self, changer_role, user, enabled):
        self.validate_changer_role(changer_role, user.role)
        user.enabled = enabled
        db.session.add(user)

    def set_name(self, changer_role, user, name):
        self.validate_changer_role(changer_role, user.role)
        user.name = name
        db.session.add(user)

    def validate_changer_role(self, changer_role, user_role):
        return DbUser.validator().validate_changer_role(changer_role, user_role)

    def validate_role_set(self, new_role, changer_role):
        return DbUser.validator().validate_role_set(new_role, changer_role)

    def register(self, changer_role, form):
        self.validate_role_set(form.role, changer_role)
        
        user = DbUser()
        user.role = form.role
        user.username = form.username
        if form.password:
            user.password = form.password
        user.name = form.name
        user.email = form.email

        db.session.add(user)
        return user

    def verify_email(self, user, email_secret_2, email, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        if user.has_password:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)

        self.set_email(TUserRole.SUPER_ADMIN, user, email)
        self.set_password(TUserRole.SUPER_ADMIN, user, password)
        user.verified = True
        db.session.add(user)

    def change_email(self, user, email_secret_2, email, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        if not user.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        if not user.verify_password(password):
            raise TAuthError(TAuthErrorCode.PASSWORD_SALAH)

        self.set_email(TUserRole.SUPER_ADMIN, user, email)
        user.verified = True
        db.session.add(user)

    def reset_password(self, user, email_secret_2, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED)
        if not user.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)

        self.set_password(TUserRole.SUPER_ADMIN, user, password)

    def set_verified(self, changer_role, user, verified):
        self.validate_changer_role(changer_role, user.role)
        if not user.password:
            raise TUserManagementError(TUserManagementErrorCode.PASSWORD_EMPTY)
        user.verified = verified
        db.session.add(user)

    def delete(self, changer_role, user):
        self.validate_changer_role(changer_role, user.role)
        if user.verified:
            raise TUserManagementError(TUserManagementErrorCode.CANNOT_DELETE_VERIFIED)
        db.session.delete(user)
