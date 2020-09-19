from flask import request

from rpc.gen.user.recovery.services import TUserRecoveryService
from rpc.gen.user.email.errors.ttypes import TEmailError, TEmailErrorCode

from models import get_model
from converter.user import DBUser_TUser

class TUserRecoveryServiceHandler(TUserRecoveryService.Iface):
    def __init__(self):
        self.user_model = get_model('user')
        
    def reset_password(self, username):
        ip = request.remote_addr
        self.user_model.send_reset_password(ip, username)

    def resend_verification(self, username):
        ip = request.remote_addr
        self.user_model.resend_verify_email(ip, username)