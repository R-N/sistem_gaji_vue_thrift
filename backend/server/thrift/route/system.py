from ..thrift import add_route
from rpc.gen.system.backup.services import TSystemBackupService
from rpc.handler.system.backup import TSystemBackupServiceHandler


def init(app):
    add_route(app, '/api/system/backup', TSystemBackupService, TSystemBackupServiceHandler)
    
    return app
