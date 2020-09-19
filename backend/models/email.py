import os
from dotenv import load_dotenv
from emails.template import JinjaTemplate as Template

from rpc.gen.user.email.errors.ttypes import TEmailError, TEmailErrorCode

from .manager import basic_models
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()


MESSAGE_NEW_ACCOUNT = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda telah didaftarkan pada Sistem Gaji dengan username '{{ username }}'.
        Untuk dapat menggunakan akun Anda, mohon konfirmasi email Anda.
        Anda dapat meminta link konfirmasi pada halaman login.
    </p>
    <p>
        <a href="{{ base_url }}">Halaman login</a>
    </p>
'''

MESSAGE_VERIFY_NEW_ACCOUNT = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda telah didaftarkan pada Sistem Gaji.
        Untuk dapat menggunakan akun Anda, mohon konfirmasi email Anda.
        Link hanya berlaku selama 2 jam dan hanya untuk IP Anda.
    </p>
    <p>
        <a href="{{ base_url }}/verifyemail/{{ token }}">Konfirmasi</a>
    </p>
'''

MESSAGE_VERIFY_CHANGE_EMAIL = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda meminta untuk mengubah alamat email Anda pada Sistem Gaji.
        Jika ini benar, mohon konfirmasi.
        Link hanya berlaku selama 2 jam dan hanya untuk IP Anda.
    </p>
    <p>
        <a href="{{ base_url }}/verifyemail/{{ token }}">Konfirmasi</a>
    </p>
'''
MESSAGE_RESET_PASSWORD = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda meminta untuk me-reset password Anda.
        Silahkan ikuti link berikut untuk melanjutkan.
        Link hanya berlaku selama 2 jam dan hanya untuk IP Anda.
    </p>
    <p>
        <a href="{{ base_url }}/resetpassword/{{ token }}">Reset Password</a>
    </p>
'''
MESSAGE_VERIFY_EMAIL_SUCCEEDED = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda telah berhasil memverifikasi email Anda. Selamat datang di Sistem Gaji.
    </p>
    <p>
        <a href="{{ base_url }}">Login</a>
    </p>
'''
MESSAGE_CHANGE_EMAIL_SUCCEEDED = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda telah mengganti email Anda dari:
    </p>
    <p>
        {{ old_email }}
    </p>
    <p> 
        Menjadi:
    </p>
    <p>
        {{ email }}
    </p>
    <p>
        Jika ini adalah sebuah kesalahan,
        segera ganti password dan kembalikan email,
        atau hubungi admin.
    </p>
'''

MESSAGE_CHANGE_PASSWORD_SUCCEEDED = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda telah mengganti password Anda.
    </p>
    <p>
        Jika ini adalah sebuah kesalahan,
        segera reset password,
        atau hubungi admin.
    </p>
'''
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
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_INVALID:
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID)
            raise

    def decode_password(self, ip, token):
        try:
            return self.basic.decode(self.func_password, ip, token)
        except TEmailError as ex:
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED:
                raise TEmailError(TEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED)
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_INVALID:
                raise TEmailError(TEmailErrorCode.RESET_PASSWORD_TOKEN_INVALID)
            raise

    def send_welcome_email(self, user, html=MESSAGE_NEW_ACCOUNT):
        html = Template(html)
        msg = self.basic.make_email("Pendaftaran Akun Sistem Gaji", html)
        data = self.basic.base_user_data(user)
        return self.basic.send_email(msg, user.email, render=data)

    def send_change_email(self, ip, user, email, html=MESSAGE_VERIFY_CHANGE_EMAIL):
        email_secret_2 = self.basic.make_secret(user, self.func_verify)

        payload = {
            'user_id': user.id,
            'email': email,
            'email_secret_2': email_secret_2
        }

        subject = "Konfirmasi email akun Sistem Gaji"
        token = self.encode_verify(ip, payload)

        html = Template(html)
        msg = self.basic.make_email(subject, html)

        data = self.basic.base_user_data(user)
        data['token'] = token

        return self.basic.send_email(msg, email, render=data)

    def send_verify_email(self, ip, user, html=MESSAGE_VERIFY_NEW_ACCOUNT):
        return self.send_change_email(ip, user, user.email, html=html)

    def send_change_email_succeeded(self, user, old_email, html=MESSAGE_CHANGE_EMAIL_SUCCEEDED):
        html = Template(html)
        msg = self.basic.make_email("Perubahan Email Akun Sistem Gaji Berhasil", html)
        data = self.basic.base_user_data(user)
        data['old_email'] = old_email
        r1 = self.basic.send_email(msg, old_email, render=data)
        r2 = self.basic.send_email(msg, user.email, render=data)
        return r1, r2

    def send_change_password_succeeded(self, user, html=MESSAGE_CHANGE_PASSWORD_SUCCEEDED):
        html = Template(html)
        msg = self.basic.make_email("Perubahan Password Akun Sistem Gaji Berhasil", html)
        data = self.basic.base_user_data(user)
        return self.basic.send_email(msg, user.email, render=data)

    def send_verify_email_succeeded(self, user, html=MESSAGE_VERIFY_EMAIL_SUCCEEDED):
        html = Template(html)
        msg = self.basic.make_email("Verifikasi Email Akun Sistem Gaji Berhasil", html)
        data = self.basic.base_user_data(user)
        return self.basic.send_email(msg, user.email, render=data)

    def send_reset_password(self, ip, user, html=MESSAGE_RESET_PASSWORD):
        email_secret_2 = self.basic.make_secret(user, self.func_password)

        payload = {
            'user_id': user.id,
            'email_secret_2': email_secret_2
        }

        subject = "Reset password akun Sistem Gaji"
        token = self.encode_password(ip, payload)

        html = Template(html)
        msg = self.basic.make_email(subject, html)

        data = self.basic.base_user_data(user)
        data['token'] = token

        return self.basic.send_email(msg, user.email, render=data)