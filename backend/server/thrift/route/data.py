from ..thrift import add_route

from rpc.gen.data.perusahaan.services import TDataPerusahaanService
from rpc.handler.data.perusahaan import TDataPerusahaanServiceHandler

from rpc.gen.data.departemen.services import TDataDepartemenService
from rpc.handler.data.departemen import TDataDepartemenServiceHandler

from rpc.gen.data.job_level.services import TDataJobLevelService
from rpc.handler.data.job_level import TDataJobLevelServiceHandler

def init(app):
    add_route(app, '/api/data/perusahaan', TDataPerusahaanService, TDataPerusahaanServiceHandler)
    add_route(app, '/api/data/departemen', TDataDepartemenService, TDataDepartemenServiceHandler)
    add_route(app, '/api/data/job-level', TDataJobLevelService, TDataJobLevelServiceHandler)

    return app
