from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
import os
from dotenv import load_dotenv
import json
load_dotenv()

frontend = Flask("sistem_gaji_frontend", template_folder='frontend', static_folder='frotnend/static')

BACKEND_HTTPS = bool(os.getenv("BACKEND_HTTPS") or True)
BACKEND_HOST = os.getenv("BACKEND_HOST")
BACKEND_PORT = int(os.getenv("BACKEND_PORT") or "443")

def init(app, backend_https=BACKEND_HTTPS, backend_host=BACKEND_HOST, backend_port=BACKEND_PORT):
    backend_json = json.dumps({
        'https': backend_https,
        'scheme': 'https' if backend_https else 'http',
        'host': backend_host,
        'port': backend_port
    })
    def backend_info():
        return backend_json

    def index(u_path=''):
        return render_template(
            'index.html', 
            backend_https=backend_https, 
            backend_host=backend_host, 
            backend_port=backend_port
        )
    app.route('/backend', methods=['GET'])(backend_info)
    app.route('/', defaults={'u_path': ''}, methods=['GET'])(app.route('/<path:u_path>', methods=['GET'])(index))
    return app

DEFAULT_FRONTEND_PORT = int(os.getenv("FRONTEND_PORT") or "80")

def serve(app, port=DEFAULT_FRONTEND_PORT):
    http_server = WSGIServer(('', port), frontend)
    http_server.serve_forever()

def main():
    init(frontend)
    serve(frontend)

if __name__ == "__main__":
    main()