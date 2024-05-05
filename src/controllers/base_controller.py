from abc import ABCMeta
from utils.context import Context
from utils.logger import Logger


class BaseController(metaclass=ABCMeta):
    def __init__(self, context: Context, class_name: str) -> None:
        self.context: Context = context
        self.logger = Logger(context, class_name)
