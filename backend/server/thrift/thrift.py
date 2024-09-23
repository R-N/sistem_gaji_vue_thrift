from flask import request, make_response

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport

def make_server(ServiceClass, foo_handler):
    foo_processor = ServiceClass.Processor(foo_handler)
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

def add_route(app, route, ServiceClass, HandlerClass, methods=['GET', 'POST']):
    server = make_server(ServiceClass, HandlerClass())
    def handler():
        return respond(server)
    handler.__name__ = route.replace("/", "_")
    app.route(route, methods=methods)(handler)
    return app
