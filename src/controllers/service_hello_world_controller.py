from utils.context import Context
from utils.logger import Logger


class ServiceHelloWorldController:
    def __init__(self, context: Context) -> None:
        self.context: Context = context
        self.logger = Logger(context, __class__)

    def handle_request(self) -> dict:
        return {"message": "Hello world!"}
