from flask import request

from rpc.gen.user.recovery.services import TUserRecoveryService
from rpc.gen.user.user.errors.ttypes import TUserError, TUserErrorCode

from models import models
from utils.util import email_delay

class TUserRecoveryServiceHandler(TUserRecoveryService.Iface):
    def __init__(self):
        self.user_model = models['user']
        self.email_model = models['email']

    def reset_password(self, username):
        ip = request.remote_addr
        db_user = self.user_model.get_by_username_email_silent(username)
        if not db_user:
            email_delay()
            return
        self.email_model.send_reset_password(ip, db_user)
        self.user_model.commit()

    def resend_verification(self, username):
        ip = request.remote_addr
        db_user = self.user_model.get_by_username_email_silent(username)
        if not db_user:
            email_delay()
            return
        if db_user.has_password:
            raise TUserError(TUserErrorCode.USER_ALREADY_VERIFIED)
        self.email_model.send_verify_email(ip, db_user)
        self.user_model.commit()
