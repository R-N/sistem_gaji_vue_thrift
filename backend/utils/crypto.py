import hashlib
import os
from dotenv import load_dotenv
from passlib.hash import sha256_crypt, bcrypt, bcrypt_sha256
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