from ..thrift import add_route

from rpc.gen.hello.hello.services import THelloService
from rpc.handler.hello.hello import THelloServiceHandler

def init(app):
    add_route(app, '/api/hello/hello', THelloService, THelloServiceHandler)
    
    return app
