from flask import jsonify
from rpc.gen.file.upload.ttypes import TUploadError, TUploadErrorCode
from utils.file import file_allowed

def get_args(request, args, json=None):
    if json is None:
        try:
            json = request.get_json(force=True)
            return get_args(request, args, json)
        except Exception:
            return get_args(request, args, {})
    return {k: (v or request.headers.get(k) or json.get(k) or request.form.get(k) or request.args.get(k)) for k, v in args.items()}

def json_error(err, status=500):
    response = {
        'error': err.__class__.__name__,
        'code': err.code
    }
    response = jsonify(response)
    response.status_code = status
    return response

def get_file(request, name, allowed_extensions=None):
    if name not in request.files:
        raise TUploadError(TUploadErrorCode.FILE_NOT_PROVIDED)
    file = request.files[name]
    if not (file and file.filename):
        raise TUploadError(TUploadErrorCode.FILE_NOT_PROVIDED)
    if allowed_extensions and not file_allowed(file.filename, allowed_extensions):
        raise TUploadError(TUploadErrorCode.FILE_INVALID)
    return file