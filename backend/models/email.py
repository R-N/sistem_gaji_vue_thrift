import os
from dotenv import load_dotenv
import emails
from emails.template import JinjaTemplate as Template
from datetime import timedelta, datetime
import jwt

from rpc.gen.user.email.errors.ttypes import TEmailError, TEmailErrorCode

from utils.crypto import md5

from .general_key import GeneralKeyModel
# MODELS MUST ONLY USE THRIFT ENUM AND EXCEPTIONS
# MODELS MAY NOT USE THRIFT STRUCTS

load_dotenv()

DEFAULT_SMTP = {
    'host': os.getenv("SMTP_HOST") or "smtp.gmail.com",
    'port': int(os.getenv("SMTP_PORT") or "465"),
    'ssl': bool(os.getenv("SMTP_SSL") or "True"),
    'user': os.getenv("SMTP_USER"),
    'password': os.getenv("SMTP_PASSWORD")
}

DEFAULT_SENDER_NAME = os.getenv("EMAIL_SENDER_NAME") or "Emailer Sistem Gaji"

ENC_FILE = os.getenv("EMAIL_ENC")
DEC_FILE = os.getenv("EMAIL_DEC")
SECRET = os.getenv("EMAIL_SECRET")
EXPIRATION = timedelta(minutes=int(os.getenv("EMAIL_EXPIRATION_MINUTE") or "30"))

BASE_URL = os.getenv("BASE_URL") or "https://localhost"


MESSAGE_NEW_ACCOUNT = '''
    <p>
        Halo, {{ name }}
    </p>
    <p>
        Anda telah didaftarkan pada Sistem Gaji.
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
        {{ new_email }}
    </p>
    <p>
        Jika ini adalah sebuah kesalahan,
        segera ganti password dan kembalikan email,
        atau hubungi admin.
    </p>
'''

class EmailModel(GeneralKeyModel):
    def __init__(
        self, 
        secret=SECRET,
        expiration=EXPIRATION,
        enc=None,
        dec=None,
        smtp=DEFAULT_SMTP,
        sender_name=DEFAULT_SENDER_NAME,
        sender_address=None
    ):
        super(EmailModel, self).__init__(
            ENC_FILE,
            DEC_FILE,
            secret,
            expiration,
            enc=enc,
            dec=dec
        )
        self.model_name = "email"
        self.func_verify = self.model_name + ":verify"
        self.func_password = self.model_name + ":password"

        self.smtp = smtp
        self.sender_name = sender_name
        self.sender_address = sender_address or smtp['user']

    def make_email(self, subject, html):
        return emails.html(
            html=html,
            subject=subject,
            mail_from=(self.sender_name, self.sender_address)
        )

    def send_email(self, email, recepient, render={}):
        r = email.send(to=recepient, smtp=self.smtp, render=render)
        if r.status_code != 250:
            raise TEmailError(TEmailErrorCode.EMAIL_NOT_SENT)


    def decode(self, func, ip, token):
        try:
            return super(EmailModel, self).decode(func, ip, token)
        except jwt.ExpiredSignatureError:
            raise TEmailError(TEmailErrorCode.EMAIL_TOKEN_EXPIRED)
        except (jwt.InvalidIssuerError, jwt.InvalidAudienceError, jwt.DecodeError):
            raise TEmailError(TEmailErrorCode.EMAIL_TOKEN_INVALID)

    def encode_verify(self, ip, payload):
        return self.encode(self.func_verify, ip, payload)

    def encode_password(self, ip, payload):
        return self.encode(self.func_password, ip, payload)

    def decode_verify(self, ip, token):
        try:
            return self.decode(self.func_verify, ip, token)
        except TEmailError as ex:
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED:
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_EXPIRED)
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_INVALID:
                raise TEmailError(TEmailErrorCode.EMAIL_VERIFICATION_TOKEN_INVALID)
            raise

    def decode_password(self, ip, token):
        try:
            return self.decode(self.func_password, ip, token)
        except TEmailError as ex:
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_EXPIRED:
                raise TEmailError(TEmailErrorCode.RESET_PASSWORD_TOKEN_EXPIRED)
            if ex.code == TEmailErrorCode.EMAIL_TOKEN_INVALID:
                raise TEmailError(TEmailErrorCode.RESET_PASSWORD_TOKEN_INVALID)
            raise

    def make_secret(self, session, user, func, now=None):
        now = now or datetime.utcnow()
        now_ts = str(now.timestamp())
        email_secret_2 = md5(str(user.id) + func + now_ts)

        user.set_email_secret_2(email_secret_2)
        session.add(user)
        session.commit()
        session.refresh(user)
        return email_secret_2

    def send_email_2(self, token, user, payload, subject, html, email):

        html = Template(html)
        msg = self.make_email(subject, html)
        data = {
            'name': user.name,
            'base_url': BASE_URL,
            'token': token
        }
        return self.send_email(msg, email, render=data)

    def send_welcome_email(self, user, html=MESSAGE_NEW_ACCOUNT):
        html = Template(html)
        msg = self.make_email("Pendaftaran Akun Sistem Gaji", html)
        data = {
            'name': user.name,
            'base_url': BASE_URL
        }
        return self.send_email(msg, user.email, render=data)


    def send_change_email(self, session, ip, user, email, html=MESSAGE_VERIFY_CHANGE_EMAIL):
        return self.send_verify_email(session, ip, user, email, html=html)

    def send_verify_email(self, session, ip, user, email, html=MESSAGE_VERIFY_NEW_ACCOUNT):
        email_secret_2 = self.make_secret(session, user, self.func_verify)

        payload = {
            'user_id': user.id,
            'email': email,
            'email_secret_2': email_secret_2
        }

        subject = "Konfirmasi email akun Sistem Gaji"
        token = self.encode_verify(ip, payload)
        return self.send_email_2(token, user, payload, subject, html, email)


    def send_change_email_succeeded(self, user, old_email, html=MESSAGE_CHANGE_EMAIL_SUCCEEDED):
        html = Template(html)
        msg = self.make_email("Perubahan Email Akun Sistem Gaji Berhasil", html)
        data = {
            'name': user.name,
            'base_url': BASE_URL,
            'old_email': old_email,
            'new_email': user.email
        }
        r1 = self.send_email(msg, old_email, render=data)
        r2 = self.send_email(msg, user.email, render=data)
        return r1, r2

    def send_reset_password(self, session, ip, user, html=MESSAGE_RESET_PASSWORD):
        email_secret_2 = self.make_secret(session, user, self.func_password)

        payload = {
            'user_id': user.id,
            'email_secret_2': email_secret_2
        }

        subject = "Reset password akun Sistem Gaji"
        token = self.encode_password(ip, payload)
        return self.send_email_2(token, user, payload, subject, html, user.email)