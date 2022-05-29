import hashlib
import os
from dotenv import load_dotenv
from passlib.hash import sha256_crypt, bcrypt, bcrypt_sha256
import jwt
from datetime import datetime
load_dotenv()


def md5(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest()

def hash_sha256(text):
    return sha256_crypt.hash(text)

def verify_sha256(hash, text):
    return sha256_crypt.verify(text, hash)

def hash_bcrypt(text):
    return bcrypt.hash(text)

def verify_bcrypt(hash, text):
    return bcrypt.verify(text, hash)

def hash_bcrypt_sha256(text):
    return bcrypt_sha256.hash(text)

def verify_bcrypt_sha256(hash, text):
    return bcrypt_sha256.verify(text, hash)

def encode_jwt(payload, enc, expiration, now=None):
    now = now or datetime.utcnow()
    payload['exp'] = now + expiration
    return jwt.encode(payload, enc, algorithm='RS256')  # .decode('utf-8')

def decode_jwt(token, dec, issuer=None, audience=None):
    return jwt.decode(token.decode('utf-8') if token is str else token, dec, algorithms='RS256', issuer=issuer, audience=audience)