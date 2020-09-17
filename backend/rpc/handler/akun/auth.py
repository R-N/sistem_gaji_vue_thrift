from rpc.gen.akun.auth import TAuthService
from models import get_model
from rpc.gen.akun.auth.ttypes import TLoginResult
from flask import request

class TAuthServiceHandler(TAuthService.Iface):
    def __init__(self):
        self.auth_model = get_model('auth')
        self.user_model = get_model('user')

    def login(self, username, password):
        return TLoginResult(*self.auth_model.login(username, password))

    def refresh_auth(self, auth_token, refresh_token):
        return self.auth_model.refresh_auth(auth_token, refresh_token)

    def reset_password(self, username):
        ip = request.remote_addr
        self.user_model.send_reset_password(ip, username)

    def resend_verification(self, username):
        ip = request.remote_addr
        self.user_model.resend_verify_email(ip, username)
        