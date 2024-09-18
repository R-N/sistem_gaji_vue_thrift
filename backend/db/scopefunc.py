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
        try:
            from flask._app_ctx_stack import __ident_func__ as _ident_func
        except ImportError:
            try:
                from greenlet import getcurrent as _ident_func
            except ImportError:
                from threading import get_ident as _ident_func

        SCOPEFUNC = _ident_func
    return SCOPEFUNC
