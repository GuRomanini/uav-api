import logging
import sys
import os
import json
import datetime

from utils.singleton import Singleton
from utils.context import Context

from constants import SERVICE_NAME, APP_ENV

urllib3_log = logging.getLogger("google")
urllib3_log.setLevel(logging.CRITICAL)
urllib3_log.propagate = True

uvi_log = logging.getLogger("uvicorn.error")
uvi_log.setLevel(logging.CRITICAL)
uvi_log.propagate = True

urllib3_log = logging.getLogger("urllib3")
urllib3_log.setLevel(logging.CRITICAL)
urllib3_log.propagate = True
logging.getLogger("chardet.charsetprober").setLevel(logging.INFO)

asyncio_log = logging.getLogger("asyncio")
asyncio_log.setLevel(logging.CRITICAL)
asyncio_log.propagate = True


class BaseClassWithLogger:

    __slots__ = "logger"

    def __init__(self, class_name=None):
        self.logger = Logger(class_name)


class Logger:
    def __init__(self, context: Context, class_name):
        self.context = context
        self.handler = LogHandler().get_logger(class_name)

    def debug(self, msg, message_json={}):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.debug(log_json)

    def info(self, msg, message_json={}):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.info(log_json)

    def warning(self, msg, message_json={}):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.warning(log_json)

    def error(self, msg, message_json={}):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.error(log_json)

    def fatal(self, msg, message_json={}):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.fatal(log_json)

    def __prepare_log(self, msg, message_json):
        log_json = dict()
        log_json["message"] = msg
        log_json["message_json"] = message_json
        log_json["global_trace_id"] = self.context.global_trace_id
        log_json["operations"] = self.context.operations
        if APP_ENV.upper() in ("LOCAL", "TEST"):
            return f"{msg} - {message_json}"
        return json.dumps(log_json)


class LogHandler(metaclass=Singleton):
    def __init__(self) -> None:
        self.__setup_root_logger()

    def get_logger(self, class_name):
        logger_name = f"{SERVICE_NAME}.{class_name}"
        logger = logging.getLogger(logger_name)
        return logger

    def __setup_root_logger(self):
        logger = logging.getLogger()

        log_level = logging.DEBUG
        logger.setLevel(log_level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = StackdriverFormatter()

        handler.setFormatter(formatter)
        logger.addHandler(handler)


class StackdriverFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(StackdriverFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        log_msg = record.getMessage()

        try:
            payload = json.loads(log_msg)
        except Exception:
            payload = dict()
            payload["message"] = log_msg
            payload["message_json"] = {}
            payload["global_trace_id"] = None
            payload["operations"] = None

        pid = str(os.getpid())
        message = payload["message"]
        message_j = payload.get("message_json")
        if APP_ENV.upper() in ("LOCAL", "TEST"):
            return f"[{pid} - {record.levelname}] {message} - {message_j}"

        log_record = dict()
        log_record["global_trace_id"] = payload["global_trace_id"]
        log_record["operations"] = payload["operations"]
        log_record["severity"] = record.levelname
        log_record["name"] = record.name
        log_record["pid"] = pid
        log_record["timestamp"] = str(datetime.datetime.utcnow())
        log_record["message"] = message
        log_record["message_json"] = message_j

        return json.dumps(log_record)
