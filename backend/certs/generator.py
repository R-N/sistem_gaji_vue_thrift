import os
from OpenSSL import crypto
from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
COMMON_NAME = os.getenv("COMMON_NAME")
COUNTRY_NAME = os.getenv("COUNTRY_NAME")
LOCALITY_NAME = os.getenv("CITY_NAME")
STATE_OR_PROVINCE_NAME = os.getenv("PROVINCE_NAME")
ORGANIZATION_NAME = os.getenv("ORGANIZATION_NAME")
ORGANIZATION_UNIT_NAME = os.getenv("ORGANIZATION_UNIT_NAME")
CRT_VALIDITY = int(os.getenv("CRT_VALIDITY_YEARS")) * 365 * 24 * 60 * 60

def make_key():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    return k

def make_crt(
    key=None,
    emailAddress=EMAIL_ADDRESS,
    commonName=COMMON_NAME,
    countryName=COUNTRY_NAME,
    localityName=LOCALITY_NAME,
    stateOrProvinceName=STATE_OR_PROVINCE_NAME,
    organizationName=ORGANIZATION_NAME,
    organizationUnitName=ORGANIZATION_UNIT_NAME,
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=CRT_VALIDITY
):
    #can look at generated file using openssl:
    #openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    key = key or make_key()
    # create a self-signed crt
    crt = crypto.X509()
    crt.get_subject().C = countryName
    crt.get_subject().ST = stateOrProvinceName
    crt.get_subject().L = localityName
    crt.get_subject().O = organizationName
    crt.get_subject().OU = organizationUnitName
    crt.get_subject().CN = commonName
    crt.get_subject().emailAddress = emailAddress
    crt.set_serial_number(serialNumber)
    crt.gmtime_adj_notBefore(0)
    crt.gmtime_adj_notAfter(validityEndInSeconds)
    crt.set_issuer(crt.get_subject())
    crt.set_pubkey(key)
    return crt

def make_key_crt(signing_key=None, **kwargs):
    key = make_key()
    crt = make_crt(key, **kwargs)
    signing_key = signing_key or key
    crt.sign(signing_key, 'sha512')
    return key, crt
    
def pem_priv_key(key):
    return crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("utf-8")

def pem_pub_key(key):
    return crypto.dump_publickey(crypto.FILETYPE_PEM, key).decode("utf-8")

def pem_crt(crt):
    return crypto.dump_certificate(crypto.FILETYPE_PEM, crt).decode("utf-8")

def text_crt(crt):
    return crypto.dump_certificate(crypto.FILETYPE_TEXT, crt).decode("utf-8")

def p12_key_crt(key, crt, password):
    pfx = crypto.PKCS12()
    pfx.set_privatekey(key)
    pfx.set_certificate(crt)
    return pfx.export(password.encode('utf-8'))

def export_key_crt(
    key,
    crt,
    key_file=None,
    crt_file=None,
    pem_file=None,
    p12_file=None,
    p12_password=None,
    ca_file=None
):
    key_str = pem_priv_key(key)
    if key_file:
        with open(key_file, "wt") as f:
            f.write(key_str)
    crt_str = pem_crt(crt)
    if crt_file:
        with open(crt_file, "wt") as f:
            f.write(crt_str)
    pem_str = crt_str + key_str
    if pem_file:
        with open(pem_file, "wt") as f:
            f.write(pem_str)
    if p12_file:
        if not p12_password:
            raise Exception("Please provide p12_password to export p12_file")
        p12_str = p12_key_crt(key, crt, p12_password)
        with open(p12_file, "wb") as f:
            f.write(p12_str)
    if ca_file:
        ca_str = text_crt(crt)
        with open(ca_file, "wt") as f:
            f.write(ca_str)

SERVER_KEY = os.getenv("SERVER_KEY")
SERVER_CRT = os.getenv("SERVER_CRT")
SERVER_PEM = os.getenv("SERVER_PEM")
SERVER_P12 = os.getenv("SERVER_P12")
SERVER_CA = os.getenv("SERVER_CA")
SERVER_P12_PASSWORD = os.getenv("SERVER_P12_PASSWORD")

def generate_server(
    defaults=True,
    key_file=None,
    crt_file=None,
    pem_file=None,
    p12_file=None,
    p12_password=None,
    ca_file=None,
    **kwargs
):
    if defaults:
        key_file = key_file or SERVER_KEY
        crt_file = crt_file or SERVER_CRT
        pem_file = pem_file or SERVER_PEM
        p12_file = p12_file or SERVER_P12
        p12_password = p12_password or SERVER_P12_PASSWORD
        ca_file = ca_file or SERVER_CA

    key, crt = make_key_crt(**kwargs)

    export_key_crt(
        key,
        crt,
        key_file=key_file,
        crt_file=crt_file,
        pem_file=pem_file,
        p12_file=p12_file,
        p12_password=p12_password,
        ca_file=ca_file
    )

    return key, crt

def export_key(key, priv_file=None, pub_file=None):
    priv_str = pem_priv_key(key)
    if priv_file:
        with open(priv_file, "wt") as f:
            f.write(priv_str)

    pub_str = pem_pub_key(key)
    if pub_file:
        with open(pub_file, "wt") as f:
            f.write(pub_str)
    return priv_str, pub_str


AUTH_ENC = os.getenv("AUTH_ENC")
AUTH_DEC = os.getenv("AUTH_DEC")

def generate_auth(enc_file=AUTH_ENC, dec_file=AUTH_DEC):
    key = make_key()
    enc, dec = export_key(key, priv_file=enc_file, pub_file=dec_file)
    return enc, dec

REFRESH_ENC = os.getenv("REFRESH_ENC")
REFRESH_DEC = os.getenv("REFRESH_DEC")

def generate_refresh(enc_file=REFRESH_ENC, dec_file=REFRESH_DEC):
    key = make_key()
    enc, dec = export_key(key, priv_file=enc_file, pub_file=dec_file)
    return enc, dec

if __name__ == "__main__":
    generate_server()
    generate_auth()
    generate_refresh()