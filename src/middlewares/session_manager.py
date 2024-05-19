from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from constants import (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_PORT,
    BYPASS_ENDPOINTS,
)


class SessionManager:
    path = "mysql+pymysql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    engine = create_engine(path, echo=False, pool_recycle=3600)
    session_class = sessionmaker(bind=engine, autoflush=False)
    ThreadSession = scoped_session(session_class)

    def process_resource(self, req, resp, resource, params):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return
        req.context.instance.add_session(SessionManager.ThreadSession())

    def process_response(self, req, resp, resource, req_succeeded):
        if req.context.instance.db_session is not None:
            if not req_succeeded:
                req.context.instance.db_session.rollback()
            req.context.instance.db_session.close()
