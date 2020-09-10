from pathlib import Path
from flask import safe_join
from werkzeug.exceptions import NotFound
from rpc.gen.file.file.ttypes import TFileError, TFileErrorCode

def file_exists(file_dir, file_name):
    try:
        file = (Path(file_dir) / file_name).resolve()
        parent = Path(file_dir).resolve()
        if file.parent != parent:
            raise TFileError(TFileErrorCode.FILE_NAME_INVALID)
        file_2 = Path(safe_join(file_dir, file_name))
        if file != file_2.resolve():
            raise TFileError(TFileErrorCode.FILE_NAME_INVALID)
        return file_2.is_file()
    except NotFound:
        raise TFileError(TFileErrorCode.FILE_NAME_INVALID)

def file_allowed(file_name, allowed_extensions):
    #file_name = secure_filename(file_name)
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in allowed_extensions
