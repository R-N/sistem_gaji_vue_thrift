from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
import os
from dotenv import load_dotenv
import json
import socket
load_dotenv()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

frontend = Flask("sistem_gaji_frontend", template_folder='frontend', static_folder='frotnend/static')

MY_IP = get_ip()
BACKEND_HTTPS = bool(os.getenv("BACKEND_HTTPS") or True)
BACKEND_HOST = os.getenv("BACKEND_HOST") or MY_IP
BACKEND_PORT = int(os.getenv("BACKEND_PORT") or "443")

def init(app, backend_https=BACKEND_HTTPS, backend_host=BACKEND_HOST, backend_port=BACKEND_PORT):
    print("Backend host: " + BACKEND_HOST)
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