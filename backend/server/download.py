from flask import request, jsonify, send_from_directory, safe_join, abort
import json
from models import get_model
from thrift.Thrift import TException


def download(download_token=''):
    download_token = download_token 
    if not download_token:
        try:
            post_json = request.get_json(force=True)
            print("post_json: " + str(post_json))
            if 'download_token' in post_json:
                download_token = post_json['download_token']
        except Exception:
            pass
    if not download_token and 'download_token' in request.form:
        download_token = request.form['download_token']
    if not download_token and 'download_token' in request.args:
        download_token = request.args['download_token']
    print("token: " + str(download_token))
    ip = request.remote_addr
    try:
        payload = get_model('download').decode(ip, download_token)
        return send_from_directory(payload['dir'], filename=payload['name'], as_attachment=True)
    except TException as err:
        response = {
            'error': str(type(err)),
            'code': err.code
        }
        response = jsonify(response)
        response.status_code = 500
        return response

def init(app):
    app.route('/download/<download_token>', methods=["POST", "GET"])(download)
    app.route('/download/', methods=["POST", "GET"])(download)
    app.route('/download', methods=["POST", "GET"])(download)
