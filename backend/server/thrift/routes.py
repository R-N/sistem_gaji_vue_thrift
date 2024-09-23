from .route import data, hello, system, user

def init(app):
    data.init(app)
    hello.init(app)
    system.init(app)
    user.init(app)
