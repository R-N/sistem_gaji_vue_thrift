from flask import request, make_response

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport

from rpc.gen.akun.auth import TAuthService
from rpc.handler.akun.auth import TAuthServiceHandler

from rpc.gen.akun.user import TUserService
from rpc.handler.akun.user import TUserServiceHandler

from rpc.gen.akun.akun import TAkunService
from rpc.handler.akun.akun import TAkunServiceHandler

from rpc.gen.hello.hello import THelloService
from rpc.handler.hello.hello import THelloServiceHandler

from rpc.gen.system.backup import TBackupService
from rpc.handler.system.backup import TBackupServiceHandler

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

auth_server = make_server(TAuthService, TAuthServiceHandler())
def akun_auth():
    return respond(auth_server)

user_server = make_server(TUserService, TUserServiceHandler())
def akun_user():
    return respond(user_server)

akun_server = make_server(TAkunService, TAkunServiceHandler())
def akun_akun():
    return respond(akun_server)

hello_server = make_server(THelloService, THelloServiceHandler())
def hello_hello():
    return respond(hello_server)

backup_server = make_server(TBackupService, TBackupServiceHandler())
def system_backup():
    return respond(backup_server)

def init(app):
    app.route('/api/akun/auth', methods=['POST'])(akun_auth)
    app.route('/api/akun/user', methods=['POST'])(akun_user)
    app.route('/api/akun/akun', methods=['POST'])(akun_akun)
    app.route('/api/hello/hello', methods=['POST'])(hello_hello)
    app.route('/api/system/backup', methods=['POST'])(system_backup)
    return app
