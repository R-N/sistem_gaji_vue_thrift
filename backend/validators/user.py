from db import DBSession
import db.entities as entities

from rpc.gen.akun.user.ttypes import TUserError, TUserErrorCode
from rpc.gen.akun.auth.ttypes import TUserRole, TAuthError, TAuthErrorCode
import re 
  
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

EMAIL_REGEX_STR = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
EMAIL_REGEX = re.compile(EMAIL_REGEX_STR)

PASSWORD_REGEX_STR = '^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
PASSWORD_REGEX = re.compile(PASSWORD_REGEX_STR)

def _validate_role(role):
    if role is None:
        raise TUserError(TUserErrorCode.ROLE_EMPTY)
    if role not in TUserRole._VALUES_TO_NAMES:
        raise TUserError(TUserErrorCode.ROLE_INVALID)

def validate_role(role, my_role=None):
    _validate_role(role)
    if role == TUserRole.SUPER_ADMIN and (my_role != TUserRole.SUPER_ADMIN or not my_role):
        raise TAuthError(TAuthErrorCode.ROLE_INVALID)

def validate_email(email, session=None):
    if not session:
        with DBSession() as session:
            return validate_email(email, session)
    if not email:
        raise TUserError(TUserErrorCode.EMAIL_EMPTY)
    if not EMAIL_REGEX.search(email):
        raise TUserError(TUserErrorCode.EMAIL_INVALID)
    if session.query(entities.DBUser.id).filter(entities.DBUser.email == email).scalar() is not None:
        raise TUserError(TUserErrorCode.EMAIL_ALREADY_EXISTS)

def validate_password(password):
    if not password:
        raise TUserError(TUserErrorCode.PASSWORD_EMPTY)
    if not PASSWORD_REGEX.search(password):
        raise TUserError(TUserErrorCode.PASSWORD_INVALID)

def validate_name(name):
    if not name:
        raise TUserError(TUserErrorCode.NAME_EMPTY)

def validate_username(username, session=None):
    if not session:
        with DBSession() as session:
            return validate_username(username, session)
    if not username:
        raise TUserError(TUserErrorCode.USERNAME_EMPTY)
    if session.query(entities.DBUser.id).filter(entities.DBUser.username == username).scalar() is not None:
        raise TUserError(TUserErrorCode.USERNAME_ALREADY_EXISTS)

