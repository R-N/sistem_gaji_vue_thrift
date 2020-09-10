from pathlib import Path
from flask import safe_join

def file_exists(file_dir, file_name=None):
    if file_name:
        file = Path(safe_join(file_dir, file_name))
    else:
        file = Path(file_dir)
    return file.is_file()

def file_allowed(file_name, allowed_extensions):
    #file_name = secure_filename(file_name)
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in allowed_extensions
