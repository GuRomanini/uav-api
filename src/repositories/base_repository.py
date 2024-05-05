from abc import ABCMeta
from sqlalchemy.orm.query import Query

from utils.context import Context
from utils.logger import Logger


class BaseRepository(metaclass=ABCMeta):
    def __init__(self, context: Context, class_name: str) -> None:
        self.__session = context.db_session
        self.logger = Logger(context, class_name)

    def flush(self) -> None:
        self.__session.flush()

    def commit(self) -> None:
        self.__session.commit()

    def rollback(self) -> None:
        self.__session.rollback()

    def add(self, model) -> None:
        self.__session.add(model)

    def query(self, *models) -> Query:
        return self.__session.query(*models)

    def get_enumerator(self, model, enumerator):
        return self.__session.query(model).filter(model.enumerator == enumerator).one()

    def get_enumerators(self, model, enumerators: list):
        return self.__session.query(model).filter(model.enumerator.in_(enumerators)).all()
