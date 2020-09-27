import os
from dotenv import load_dotenv
load_dotenv()

IS_FLASK_APP = False
SCOPEFUNC = None

def get_scopefunc():
    global IS_FLASK_APP
    global SCOPEFUNC

    is_flask_app_str = os.getenv("IS_FLASK_APP")
    IS_FLASK_APP = bool(is_flask_app_str) if is_flask_app_str else False

    if IS_FLASK_APP:
        from flask import _app_ctx_stack
        SCOPEFUNC = _app_ctx_stack.__ident_func__
    return SCOPEFUNC
