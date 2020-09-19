from flask import request

from rpc.gen.user.email.services import TUserEmailService
from rpc.gen.user.email.errors.ttypes import TEmailError, TEmailErrorCode

from models import get_model
from converter.user import DBUser_TUser

class TUserEmailServiceHandler(TUserEmailService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')
        self.email_model = get_model('email')

    def has_password(self, email_token):
        ip = request.remote_addr
        email_payload = self.email_model.decode_verify(ip, email_token)
        db_user = self.user_model.get_user(email_payload['user_id'])
        if db_user.email_secret_2 != email_payload['email_secret_2']:
            raise TEmailError(TEmailErrorCode.EMAIL_TOKEN_EXPIRED)
        return db_user.has_password

    def verify_email(self, verify_token, password):
        ip = request.remote_addr
        email_payload = self.email_model.decode_verify(ip, verify_token)
        db_user = self.user_model.verify_email(
            email_payload['user_id'],
            email_payload['email_secret_2'],
            email_payload['email'],
            password
        )

    def change_email(self, verify_token, password):
        ip = request.remote_addr
        email_payload = self.email_model.decode_verify(ip, verify_token)
        db_user = self.user_model.change_email(
            email_payload['user_id'],
            email_payload['email_secret_2'],
            email_payload['email'],
            password
        )

    def set_password(self, password_token, password):
        ip = request.remote_addr
        password_payload = self.email_model.decode_password(ip, password_token)
        db_user = self.user_model.reset_password(
            password_payload['user_id'],
            password_payload['email_secret_2'],
            password
        )
        