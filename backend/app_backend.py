from flask import Flask, request, make_response
from flask_cors import CORS

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport


from gevent.pywsgi import WSGIServer

import os
from dotenv import load_dotenv
from certs import generator

import app_frontend as frontend

load_dotenv()
if __name__ == "__main__":
    generator.generate_auth()
    generator.generate_refresh()

from rpc.gen.akun import AuthService
from rpc.handler.akun.auth import AuthServiceHandler

from rpc.gen.hello import HelloService
from rpc.handler.hello.hello import HelloServiceHandler


def make_server(service_class, foo_handler):
    foo_processor = service_class.Processor(foo_handler)
    foo_pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    foo_server = TServer.TServer(
        foo_processor,
        None, None, None,
        foo_pfactory,
        foo_pfactory)
    return foo_server

def respond(foo_server):
    itrans = TTransport.TMemoryBuffer(request.data)
    otrans = TTransport.TMemoryBuffer()
    iprot = foo_server.inputProtocolFactory.getProtocol(itrans)
    oprot = foo_server.outputProtocolFactory.getProtocol(otrans)
    foo_server.processor.process(iprot, oprot)
    return make_response(otrans.getvalue())

DEFAULT_CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(',') or [
    "http://localhost:8080",
    "http://localhost:80"
]


backend = Flask("sistem_gaji_backend", template_folder='frontend', static_folder='frontend/static')

auth_server = make_server(AuthService, AuthServiceHandler())
@backend.route('/api/akun/auth', methods=['POST'])
def akun_auth():
    respond(auth_server)

hello_server = make_server(HelloService, HelloServiceHandler())
@backend.route('/api/hello/hello', methods=['POST'])
def hello_hello():
    respond(hello_server)

def init(app, cors_origins=None):
    cors_origins = cors_origins or DEFAULT_CORS_ORIGINS
    print("CORS origins: " + str(cors_origins))
    CORS(app, resources={r"/api/*": {
        "origins": cors_origins
    }})
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
    frontend.init(backend, backend_https=BACKEND_HTTPS, backend_host=BACKEND_HOST, backend_port=BACKEND_PORT)
    serve(backend)

if __name__ == "__main__":
    main()