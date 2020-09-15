from db import DBSession
from db.entities import DBUser
from rpc.gen.akun.user.ttypes import TUserError, TUserErrorCode
from rpc.gen.akun.auth.ttypes import TUserRole, TAuthError, TAuthErrorCode
import re 
import validators.user as validator
from sqlalchemy.exc import IntegrityError
from db.errors import parse_db_error

# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

EMAIL_REGEX_STR = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
EMAIL_REGEX = re.compile(EMAIL_REGEX_STR)

PASSWORD_REGEX_STR = '^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
PASSWORD_REGEX = re.compile(PASSWORD_REGEX_STR)

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

    def fetch_users(self, query):
        with DBSession() as session:
            db_query = session.query(DBUser)
            db_query = db_query.order_by(DBUser.enabled.desc(), DBUser.name.asc())
            if query.enabled is not None:
                db_query = db_query.filter(DBUser.enabled == query.enabled)
            if query.role is not None:
                validator.__validate_role(query.role)
                db_query = db_query.filter(DBUser.role == query.role)
            if query.limit:
                db_query = db_query[query.offset:query.limit+query.offset]
            return db_query.all()

    def set_role(self, my_role, user_id, new_role):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_role(new_role)
            session.add(user)
            session.commit()

    def set_email(self, user_id, new_email):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_email(new_email)
            session.add(user)
            try:
                session.commit()
            except IntegrityError as ex:
                parsed = parse_db_error(ex)
                if parsed:
                    validator.parse_error(parsed)
                raise

    def set_password(self, user_id, new_password):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_password(new_password)
            session.add(user)
            session.commit()
            

    def set_enabled(self, user_id, new_enabled):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_enabled(new_enabled)
            session.add(user)
            session.commit()

    def set_name(self, user_id, new_name):
        with DBSession() as session:
            user = self._get_user(session, user_id)
            user.set_name(new_name)
            session.add(user)
            session.commit()


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
            try:
                session.commit()
                session.refresh(user)
                return user
            except IntegrityError as ex:
                parsed = parse_db_error(ex)
                if parsed:
                    validator.parse_error(parsed)
                raise

