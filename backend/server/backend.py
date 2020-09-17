from flask import Flask
from flask_cors import CORS

from gevent.pywsgi import WSGIServer

import os
from dotenv import load_dotenv
from certs import generator



import db
import db.entities

load_dotenv()
if __name__ == "__main__":
    generator.generate_auth()
    generator.generate_refresh()
    generator.generate_download()
    generator.generate_upload()
    generator.generate_email()

from server.frontend import init as init_frontend
from server.thrift import init as init_thrift
from server.backup import init as init_backup
from server.report import init as init_report

db.create_tables()

DEFAULT_CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(',') or [
    "http://localhost:8080",
    "http://localhost:80"
]
CORS_RESOURCES = [
    r"/api/*",
    r"/backup/*",
    r"/backend/*",
    r"/download/*",
    r"/upload/*",
    r"/report/*"
]

backend = Flask("sistem_gaji_backend", template_folder='frontend', static_folder='frontend/static')
backend.config['SQLALCHEMY_DATABASE_URI'] = db.connect_str

def init(app, cors_origins=None):
    init_thrift(app)
    init_backup(app)
    init_report(app)
    cors_origins = cors_origins or DEFAULT_CORS_ORIGINS
    print("CORS resources: " + str(CORS_RESOURCES))
    print("CORS origins: " + str(cors_origins))
    cors_origins_obj = {
        "origins": cors_origins
    }
    cors_resources = {r:cors_origins_obj for r in CORS_RESOURCES}
    CORS(app, resources=cors_resources)
    return app

SERVER_KEY = os.getenv("SERVER_KEY")
SERVER_CRT = os.getenv("SERVER_CRT")
BACKEND_HTTPS = bool(os.getenv("BACKEND_HTTPS") or True)
BACKEND_HOST = os.getenv("BACKEND_HOST")
BACKEND_PORT = int(os.getenv("BACKEND_PORT") or "443")

def serve(app, port=BACKEND_PORT, use_ssl=BACKEND_HTTPS, keyfile=SERVER_KEY, certfile=SERVER_CRT):
    if use_ssl:
        if not (keyfile and certfile):
            raise Exception("Please provide keyfile and certfile to serve with use_ssl")
        http_server = WSGIServer(('', port), backend, keyfile=keyfile, certfile=certfile)
    else:
        http_server = WSGIServer(('', port), backend)
    print("Serving backend at port %d %s ssl" % (port, "with" if use_ssl else ""))
    http_server.serve_forever()

def main():
    init(backend)
    init_frontend(backend, backend_https=BACKEND_HTTPS, backend_host=BACKEND_HOST, backend_port=BACKEND_PORT)
    serve(backend)

if __name__ == "__main__":
    main()
