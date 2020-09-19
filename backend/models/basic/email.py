import os
from dotenv import load_dotenv
import emails
from emails.template import JinjaTemplate as Template
from datetime import timedelta, datetime
import jwt

from rpc.gen.email.errors.ttypes import TEmailError, TEmailErrorCode

from utils.crypto import md5

from .general_key import GeneralKeyModel
import db
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


    def make_secret(self, user, func, now=None):
        now = now or datetime.utcnow()
        now_ts = str(now.timestamp())
        email_secret_2 = md5(str(user.id) + func + now_ts)

        user.set_email_secret_2(email_secret_2)
        db.session.add(user)
        #db.commit()
        #db.session.refresh(user)
        return email_secret_2

    def base_data(self):
        return {
            'base_url': BASE_URL
        }

    def base_user_data(self, user):
        data = self.base_data()
        data.update({
            'name': user.name,
            'username': user.username,
            'email': user.email
        })
        return data