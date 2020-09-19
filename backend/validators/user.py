import re 

from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode
from rpc.gen.user.auth.errors.ttypes import TAuthError, TAuthErrorCode
from rpc.gen.user.user.types.ttypes import TUserRole

from db.errors import parse_db_error, UniqueError
  
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

EMAIL_REGEX_STR = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
EMAIL_REGEX = re.compile(EMAIL_REGEX_STR)

PASSWORD_REGEX_STR = r'^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
PASSWORD_REGEX = re.compile(PASSWORD_REGEX_STR)

USERNAME_REGEX_STR = r'^[a-zA-Z0-9\.\_]+$'
USERNAME_REGEX = re.compile(USERNAME_REGEX_STR)

def _validate_role(role):
    if role is None:
        raise TUserError(TUserErrorCode.ROLE_EMPTY)
    if role not in TUserRole._VALUES_TO_NAMES:
        raise TUserError(TUserErrorCode.ROLE_INVALID)


def validate_changer_role(changer_role, user_role):
    return (not user_role) or user_role != TUserRole.SUPER_ADMIN or changer_role == TUserRole.SUPER_ADMIN

def validate_role(role, changer_role=None):
    _validate_role(role)
    if role == TUserRole.SUPER_ADMIN and (changer_role != TUserRole.SUPER_ADMIN or not changer_role):
        raise TAuthError(TAuthErrorCode.ROLE_INVALID)

def validate_email(email):
    if not email:
        raise TUserError(TUserErrorCode.EMAIL_EMPTY)
    if not EMAIL_REGEX.match(email):
        raise TUserError(TUserErrorCode.EMAIL_INVALID)

def validate_password(password):
    if not password:
        raise TUserError(TUserErrorCode.PASSWORD_EMPTY)
    if not PASSWORD_REGEX.match(password):
        raise TUserError(TUserErrorCode.PASSWORD_INVALID)

def validate_name(name):
    if not name:
        raise TUserError(TUserErrorCode.NAME_EMPTY)

def validate_username(username):
    if not username:
        raise TUserError(TUserErrorCode.USERNAME_EMPTY)
    if not USERNAME_REGEX.match(username):
        raise TUserError(TUserErrorCode.USERNAME_INVALID)

def parse_error(parsed):
    if isinstance(parsed, UniqueError):
        if parsed.column == "email":
            raise TUserError(TUserErrorCode.EMAIL_ALREADY_EXISTS)
        if parsed.column == "username":
            raise TUserError(TUserErrorCode.USERNAME_ALREADY_EXISTS)

def require_verified(user, verified):
    if verified and not user.verified:
        raise TUserError(TUserErrorCode.USER_UNVERIFIED)
    if not verified and user.verified:
        raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)

def require_has_password(user, has_password):
    if has_password and not user.has_password:
        raise TUserError(TUserErrorCode.USER_UNVERIFIED)
    if not has_password and user.has_password:
        raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)