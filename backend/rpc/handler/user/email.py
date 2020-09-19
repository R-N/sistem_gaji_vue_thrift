from flask import request
from sqlalchemy.exc import DBAPIError

from rpc.gen.user.email.services import TUserEmailService
from rpc.gen.user.email.errors.ttypes import TUserEmailError, TUserEmailErrorCode
from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode

from models import models

class TUserEmailServiceHandler(TUserEmailService.Iface):
    def __init__(self):
        self.auth_model = models['auth']
        self.user_model = models['user']
        self.email_model = models['email']

    def has_password(self, email_token):
        ip = request.remote_addr
        email_payload = self.email_model.decode_verify(ip, email_token)
        db_user = self.user_model.get_user_by_id(email_payload['user_id'])
        if db_user.email_secret_2 != email_payload['email_secret_2']:
            raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
        return db_user.has_password

    def verify_email(self, verify_token, password):
        ip = request.remote_addr
        email_payload = self.email_model.decode_verify(ip, verify_token)
        db_user = self.user_model.get_user_by_id(email_payload['user_id'])
        if db_user.has_password:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
        self.user_model.verify_email(
            db_user,
            email_payload['email_secret_2'],
            email_payload['email'],
            password
        )
        self.email_model.send_verify_email_succeeded(db_user)
        self.user_model.commit()

    def change_email(self, verify_token, password):
        ip = request.remote_addr
        email_payload = self.email_model.decode_verify(ip, verify_token)
        db_user = self.user_model.get_user_by_id(email_payload['user_id'])
        if not db_user.has_password:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        old_email = db_user.email
        self.user_model.change_email(
            db_user,
            email_payload['email_secret_2'],
            email_payload['email'],
            password
        )
        self.email_model.send_change_email_succeeded(db_user, old_email)
        self.user_model.commit()

    def set_password(self, password_token, password):
        ip = request.remote_addr
        password_payload = self.email_model.decode_password(ip, password_token)
        db_user = self.user_model.get_user_by_id(password_payload['user_id'])
        if not db_user.has_password:
            raise TUserError(TUserErrorCode.USER_UNVERIFIED)
        self.user_model.reset_password(
            db_user,
            password_payload['email_secret_2'],
            password
        )
        self.email_model.send_change_password_succeeded(db_user)
        self.user_model.commit()
