from sqlalchemy.orm import sessionmaker, scoped_session

def make_session(engine, scopefunc=None, autocommit=False, autoflush=False):
    session_factory = sessionmaker(autocommit=autocommit, autoflush=autoflush, bind=engine)
    return scoped_session(session_factory, scopefunc=scopefunc)
