import os
from dotenv import load_dotenv
from emails.template import JinjaTemplate as Template

from rpc.gen.email.errors.ttypes import TEmailError, TEmailErrorCode
from rpc.gen.user.email.errors.ttypes import TUserEmailError, TUserEmailErrorCode

from .manager import basic_models
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()

TEMPLATE_DIR = "email_templates/"

def read_template(filename):
    with open(TEMPLATE_DIR + filename, "rt") as f:
        return Template(f.read())

MESSAGE_WELCOME = read_template("welcome.html")
MESSAGE_VERIFY_EMAIL = read_template("verify_email.html")
MESSAGE_CHANGE_EMAIL = read_template("change_email.html")
MESSAGE_RESET_PASSWORD = read_template("reset_password.html")
MESSAGE_VERIFY_EMAIL_SUCCEEDED = read_template("verify_email_succeeded.html")
MESSAGE_CHANGE_EMAIL_SUCCEEDED = read_template("change_email_succeeded.html")
MESSAGE_CHANGE_PASSWORD_SUCCEEDED = read_template("change_password_succeeded.html")

class EmailModel:
    def __init__(self, basic=None):
        self.model_name = "email"
        self.func_verify = self.model_name + ":verify"
        self.func_password = self.model_name + ":password"
        self.basic = basic or basic_models['email']

    def encode_verify(self, ip, payload):
        return self.basic.encode(self.func_verify, ip, payload)

    def encode_password(self, ip, payload):
        return self.basic.encode(self.func_password, ip, payload)

    def decode_verify(self, ip, token):
        try:
            return self.basic.decode(self.func_verify, ip, token)
        except TEmailError as ex:
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED:
                raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_INVALID:
                raise TUserEmailError(TUserEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID)
            raise

    def decode_password(self, ip, token):
        try:
            return self.basic.decode(self.func_password, ip, token)
        except TEmailError as ex:
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED:
                raise TUserEmailError(TUserEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED)
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_INVALID:
                raise TUserEmailError(TUserEmailErrorCode.RESET_PASSWORD_TOKEN_INVALID)
            raise

    def send_welcome(self, user, body=MESSAGE_WELCOME):
        msg = self.basic.make_email("Pendaftaran Akun Sistem Gaji", body)
        data = self.basic.base_user_data(user)
        return self.basic.send_email(msg, user.email, render=data)

    def send_change_email(self, ip, user, email, body=MESSAGE_CHANGE_EMAIL):
        email_secret_2 = self.basic.make_secret(user, self.func_verify)

        payload = {
            'user_id': user.id,
            'email': email,
            'email_secret_2': email_secret_2
        }

        subject = "Konfirmasi email akun Sistem Gaji"
        token = self.encode_verify(ip, payload)

        msg = self.basic.make_email(subject, body)

        data = self.basic.base_user_data(user)
        data['token'] = token

        return self.basic.send_email(msg, email, render=data)

    def send_verify_email(self, ip, user, body=MESSAGE_VERIFY_EMAIL):
        return self.send_change_email(ip, user, user.email, body=body)

    def send_change_email_succeeded(self, user, old_email, body=MESSAGE_CHANGE_EMAIL_SUCCEEDED):
        msg = self.basic.make_email("Perubahan Email Akun Sistem Gaji Berhasil", body)
        data = self.basic.base_user_data(user)
        data['old_email'] = old_email
        r1 = self.basic.send_email(msg, old_email, render=data)
        r2 = self.basic.send_email(msg, user.email, render=data)
        return r1, r2

    def send_change_password_succeeded(self, user, body=MESSAGE_CHANGE_PASSWORD_SUCCEEDED):
        msg = self.basic.make_email("Perubahan Password Akun Sistem Gaji Berhasil", body)
        data = self.basic.base_user_data(user)
        return self.basic.send_email(msg, user.email, render=data)

    def send_verify_email_succeeded(self, user, body=MESSAGE_VERIFY_EMAIL_SUCCEEDED):
        msg = self.basic.make_email("Verifikasi Email Akun Sistem Gaji Berhasil", body)
        data = self.basic.base_user_data(user)
        return self.basic.send_email(msg, user.email, render=data)

    def send_reset_password(self, ip, user, body=MESSAGE_RESET_PASSWORD):
        email_secret_2 = self.basic.make_secret(user, self.func_password)

        payload = {
            'user_id': user.id,
            'email_secret_2': email_secret_2
        }

        subject = "Reset password akun Sistem Gaji"
        token = self.encode_password(ip, payload)

        msg = self.basic.make_email(subject, body)

        data = self.basic.base_user_data(user)
        data['token'] = token

        return self.basic.send_email(msg, user.email, render=data)