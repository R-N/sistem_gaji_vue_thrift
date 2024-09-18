from flask import request, make_response

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport

from rpc.gen.data.perusahaan.services import TDataPerusahaanService
from rpc.handler.data.perusahaan import TDataPerusahaanServiceHandler

from rpc.gen.data.departemen.services import TDataDepartemenService
from rpc.handler.data.departemen import TDataDepartemenServiceHandler

from rpc.gen.user.auth.services import TUserAuthService
from rpc.handler.user.auth import TUserAuthServiceHandler

from rpc.gen.user.recovery.services import TUserRecoveryService
from rpc.handler.user.recovery import TUserRecoveryServiceHandler

from rpc.gen.user.profile.services import TUserProfileService
from rpc.handler.user.profile import TUserProfileServiceHandler

from rpc.gen.user.management.services import TUserManagementService
from rpc.handler.user.management import TUserManagementServiceHandler

from rpc.gen.user.email.services import TUserEmailService
from rpc.handler.user.email import TUserEmailServiceHandler

from rpc.gen.hello.hello.services import THelloService
from rpc.handler.hello.hello import THelloServiceHandler

from rpc.gen.system.backup.services import TSystemBackupService
from rpc.handler.system.backup import TSystemBackupServiceHandler

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

data_perusahaan_server = make_server(TDataPerusahaanService, TDataPerusahaanServiceHandler())
def data_perusahaan():
    return respond(data_perusahaan_server)

data_departemen_server = make_server(TDataDepartemenService, TDataDepartemenServiceHandler())
def data_departemen():
    return respond(data_departemen_server)

user_auth_server = make_server(TUserAuthService, TUserAuthServiceHandler())
def user_auth():
    return respond(user_auth_server)

user_recovery_server = make_server(TUserRecoveryService, TUserRecoveryServiceHandler())
def user_recovery():
    return respond(user_recovery_server)

user_profile_server = make_server(TUserProfileService, TUserProfileServiceHandler())
def user_profile():
    return respond(user_profile_server)

user_management_server = make_server(TUserManagementService, TUserManagementServiceHandler())
def user_management():
    return respond(user_management_server)

user_email_server = make_server(TUserEmailService, TUserEmailServiceHandler())
def user_email():
    return respond(user_email_server)

hello_hello_server = make_server(THelloService, THelloServiceHandler())
def hello_hello():
    return respond(hello_hello_server)

system_backup_server = make_server(TSystemBackupService, TSystemBackupServiceHandler())
def system_backup():
    return respond(system_backup_server)

def init(app):
    app.route('/api/data/perusahaan', methods=['POST'])(data_perusahaan)
    app.route('/api/data/departemen', methods=['POST'])(data_departemen)

    app.route('/api/user/auth', methods=['POST'])(user_auth)
    app.route('/api/user/recovery', methods=['POST'])(user_recovery)
    app.route('/api/user/profile', methods=['POST'])(user_profile)
    app.route('/api/user/management', methods=['POST'])(user_management)
    app.route('/api/user/email', methods=['POST'])(user_email)

    app.route('/api/hello/hello', methods=['POST'])(hello_hello)

    app.route('/api/system/backup', methods=['POST'])(system_backup)
    
    return app
