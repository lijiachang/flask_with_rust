from flask import current_app  # 可用于确保我们的会话在Flask请求的上下文中。
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import GlobalParams


class DbEngine:
    def __init__(self):
        params = GlobalParams()
        self.base = declarative_base()
        self.engine = create_engine(params.get("DB_URL"), echo=True, pool_recycle=3600, pool_size=2, max_overflow=1,
                                    connect_args={'connect_timeout': 10})

        def get_app_context():
            return current_app._get_current_object() if current_app else None

        self.session = scoped_session(sessionmaker(bind=self.engine), scopefunc=get_app_context)
        self.url = params.get("DB_URL")


dal = DbEngine()
