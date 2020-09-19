import re 
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from time import sleep
import random
from dotenv import load_dotenv

from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode, TLoginError, TLoginErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole
from rpc.gen.user.email.errors.ttypes import TEmailError, TEmailErrorCode

from db import DBSession
from db.entities import DBUser
from db.errors import parse_db_error
import validators.user as validator

from .manager import get_model
from models.email import Template

load_dotenv()

BASE_URL = os.getenv("BASE_URL") or "https://localhost"

# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS


class UserModel:
    def __init__(self):
        pass

    def _get_user(self, session, user_id):
        user = session.query(DBUser).filter(DBUser.id == user_id).scalar()
        if not user:
            raise TUserError(TUserErrorCode.USER_NOT_FOUND)
        return user

    def get_user(self, user_id):
        with DBSession() as session:
            return self._get_user(session, user_id)

    def _get_user_by_username_email(self, session, username):
        user = session.query(DBUser).filter((DBUser.username == username) | (DBUser.email == username)).scalar()
        if not user:
            raise TUserError(TUserErrorCode.USER_NOT_FOUND)
        return user

    def get_user_by_username_email(self, username):
        with DBSession() as session:
            return self._get_user_by_username_email(session, username)

    def fetch_users(self, query):
        with DBSession() as session:
            db_query = session.query(DBUser)
            db_query = db_query.order_by(DBUser.enabled.desc(), DBUser.verified.desc(), DBUser.name.asc())
            if query.enabled is not None:
                db_query = db_query.filter(DBUser.enabled == query.enabled)
            if query.verified is not None:
                db_query = db_query.filter(DBUser.verified == query.verified)
            if query.role is not None:
                validator.__validate_role(query.role)
                db_query = db_query.filter(DBUser.role == query.role)
            if query.limit:
                db_query = db_query[query.offset:query.limit+query.offset]
            return db_query.all()

    def commit(self, session):
        try:
            session.commit()
        except IntegrityError as ex:
            parsed = parse_db_error(ex)
            if parsed:
                validator.parse_error(parsed)
            raise

    def set_role(self, my_role, user_id, new_role):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_role(new_role, my_role=my_role)
            session.add(user)
            self.commit(session)

    def set_email(self, my_role, user_id, new_email):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            if user.verified and my_role != TUserRole.SUPER_ADMIN:
                raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
            user.set_email(new_email, my_role=my_role)
            print("Done set email")
            user.set_verified(False)
            print("Done set verified")
            session.add(user)
            self.commit(session)

    def set_password(self, user_id, new_password):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_password(new_password, my_role=TUserRole.SUPER_ADMIN)
            session.add(user)
            self.commit(session)

    def set_enabled(self, my_role, user_id, new_enabled):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_enabled(new_enabled)
            session.add(user)
            self.commit(session)

    def set_name(self, my_role, user_id, new_name):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_name(new_name, my_role=my_role)
            session.add(user)
            self.commit(session)

    def send_change_email(self, ip, my_role, user_id, email):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            validator.validate_changer_role(user.role, my_role)
            get_model('email').send_change_email(session, ip, user, email)


    def resend_verify_email(self, ip, username):
        with DBSession() as session:
            try:
                user = self._get_user_by_username_email(session, username)
            except TUserError as ex:
                if ex.code == TUserErrorCode.USER_NOT_FOUND:
                    sleep(random.uniform(3, 5))
                    return
            if user.has_password:
                raise TLoginError(TLoginErrorCode.USER_ALREADY_VERIFIED)
            get_model('email').send_verify_email(session, ip, user, user.email)



    def send_reset_password(self, ip, username):
        with DBSession() as session:
            try:
                user = self._get_user_by_username_email(session, username)
            except TUserError as ex:
                if ex.code == TUserErrorCode.USER_NOT_FOUND:
                    sleep(random.uniform(3, 5))
                    return
            if not user.has_password:
                raise TLoginError(TLoginErrorCode.USER_UNVERIFIED)
            get_model('email').send_reset_password(session, ip, user)

    def register_user(self, my_role, form):
        with DBSession() as session:
            user = DBUser(
                username=form.username,
                password=form.password,
                name=form.name,
                email=form.email,
                role=form.role,
                my_role=my_role
            )
            session.add(user)
            self.commit(session)
            session.refresh(user)
            get_model('email').send_welcome_email(user)
            return user

    def verify_email(self, user_id, email_secret_2, email, password):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            if user.email_secret_2 != email_secret_2:
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
            if user.has_password:
                raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
            user.set_verified()
            user.set_email(email, my_role=TUserRole.SUPER_ADMIN)
            user.set_password(password, my_role=TUserRole.SUPER_ADMIN)
            session.add(user)
            self.commit(session)
            session.refresh(user)
            return user

    def change_email(self, user_id, email_secret_2, email, password):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            if user.email_secret_2 != email_secret_2:
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
            if not user.verified:
                raise TUserError(TUserErrorCode.USER_UNVERIFIED)
            if not user.verify_password(password):
                raise TAuthError(TAuthErrorCode.PASSWORD_SALAH)
            old_email = user.email
            user.set_email(email, my_role=TUserRole.SUPER_ADMIN)
            session.add(user)
            self.commit(session)
            session.refresh(user)
            get_model('email').send_change_email_succeeded(user, old_email)
            return user


    def reset_password(self, user_id, email_secret_2, password):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            if user.email_secret_2 != email_secret_2:
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
            if not user.verified:
                raise TUserError(TUserErrorCode.USER_UNVERIFIED)
            user.set_password(password, my_role=TUserRole.SUPER_ADMIN)
            session.add(user)
            self.commit(session)
            session.refresh(user)
            return user
