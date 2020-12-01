from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.email.errors.ttypes import TUserEmailError, TUserEmailErrorCode

import db
from db.entities.general import DbUser
import validators.user as validator

load_dotenv()

# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS


class UserModel:
    def __init__(self):
        self.validator = validator

    def parse_error(self, ex):
        validator.parse_error(ex)

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
                validator.__validate_role(query.role)
                db_query = db_query.filter(DbUser.role == query.role)
            if query.limit:
                offset = query.offset if query.offset else 0
                db_query = db_query[offset:query.limit + offset]
        return db_query.all()


    def set_role(self, changer_role, user, new_role):
        user.set_role(new_role, changer_role=changer_role)
        db.session.add(user)

    def set_email(self, changer_role, user, new_email):
        if user.verified and changer_role != TUserRole.SUPER_ADMIN:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
        user.set_email(new_email, changer_role=changer_role)
        db.session.add(user)

    def set_password(self, changer_role, user, new_password):
        user.set_password(new_password, changer_role=changer_role)
        db.session.add(user)

    def set_enabled(self, changer_role, user, new_enabled):
        user.set_enabled(new_enabled, changer_role=changer_role)
        db.session.add(user)

    def set_name(self, changer_role, user, new_name):
        user.set_name(new_name, changer_role=changer_role)
        db.session.add(user)

    def validate_changer_role(self, changer_role, user_role):
        return validator.validate_changer_role(changer_role, user_role)

    def register(self, changer_role, form):
        user = DbUser(
            username=form.username,
            password=form.password,
            name=form.name,
            email=form.email,
            role=form.role,
            changer_role=changer_role
        )
        db.session.add(user)
        return user

    def verify_email(self, user, email_secret_2, email, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        if user.has_password:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)

        self.set_email(TUserRole.SUPER_ADMIN, user, email)
        self.set_password(TUserRole.SUPER_ADMIN, user, password)
        user.set_verified(True)
        db.session.add(user)

    def change_email(self, user, email_secret_2, email, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        if not user.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        if not user.verify_password(password):
            raise TAuthError(TAuthErrorCode.PASSWORD_SALAH)

        user.set_email(email, changer_role=TUserRole.SUPER_ADMIN)
        user.set_verified(True)
        db.session.add(user)

    def reset_password(self, user, email_secret_2, password):
        if user.email_secret_2 != email_secret_2:
            raise TUserEmailError(TUserEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED)
        if not user.verified:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)

        self.set_password(TUserRole.SUPER_ADMIN, user, password)
