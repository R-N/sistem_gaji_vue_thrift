from ..thrift import add_route

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


def init(app):
    add_route(app, '/api/user/auth', TUserAuthService, TUserAuthServiceHandler)
    add_route(app, '/api/user/recovery', TUserRecoveryService, TUserRecoveryServiceHandler)
    add_route(app, '/api/user/profile', TUserProfileService, TUserProfileServiceHandler)
    add_route(app, '/api/user/management', TUserManagementService, TUserManagementServiceHandler)
    add_route(app, '/api/user/email', TUserEmailService, TUserEmailServiceHandler)
    
    return app
