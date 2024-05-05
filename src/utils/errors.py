import traceback
import falcon
from falcon import HTTPError
from abc import abstractmethod
from utils.logger import BaseClassWithLogger
from collections import OrderedDict
from functools import wraps
from constants import SERVICE_ROOT
import json


class BaseHTTPError(HTTPError):
    def __init__(self, falcon_status=None, title=None, description=None, link=None, code=None):
        HTTPError.__init__(self, falcon_status, title, description)
        self.link = link
        self.code = code

    def to_dict(self, obj_type=dict):
        obj = obj_type()
        obj["title"] = self.title
        if self.description is not None:
            obj["description"] = self.description["description"]
            obj["translation"] = self.description["translation"]
            if "traceback" in self.description:
                obj["traceback"] = self.description["traceback"]
            if "extra_fields" in self.description:
                obj["extra_fields"] = self.description["extra_fields"]
        if self.code is not None:
            obj["code"] = self.code
        if self.link is not None:
            obj["link"] = self.link
        return obj

    def to_json(self):
        obj = self.to_dict(OrderedDict)
        return json.dumps(obj, ensure_ascii=False)


class BaseError(BaseClassWithLogger):
    def __init__(self, code=None, exception=None, status=None, **kwargs):
        self.exception = exception
        BaseClassWithLogger.__init__(self)

        error_catalog_path = SERVICE_ROOT + "/utils/"
        error_catalog_filename_path = error_catalog_path + "error_catalog.json"

        with open(error_catalog_filename_path, "r") as json_catalog:
            error_object = json.load(json_catalog)

        self.description = error_object[code]  # description is actually the entire error object

        if error_object[code]["code"] == "UCS000007":  # use for rest_connector only
            self.code = kwargs["external_code"]
            self.title = kwargs["external_title"]
            self.http_status = "falcon.HTTP_" + str(status)
        else:
            self.code = error_object[code]["code"]
            self.title = error_object[code]["title"]
            self.http_status = "falcon.HTTP_" + str(error_object[code]["http_status"])

        if kwargs:
            self.description["description"] = self.description["description"].format(**kwargs)
            self.description["translation"] = self.description["translation"].format(**kwargs)
            if "extra_fields" in self.description:
                for field in self.description["extra_fields"]:
                    self.description["extra_fields"][field] = self.description["extra_fields"][field].format(**kwargs)

            self.description.setdefault("extra_fields", {}).update(kwargs)

        if self.exception is not None:
            traceback_json = _format_traceback()
            log_obj = traceback_json
            if "traceback" in self.description:  # format traceback
                self.description["traceback"] = self.description["traceback"].format(
                    traceback=traceback_json["traceback"]
                )
        else:
            log_obj = {"traceback": self.title}
        if "falcon.HTTP_5" in self.http_status:
            self.logger.fatal(log_obj)
        else:
            self.logger.error(log_obj)

    @abstractmethod
    def http(self):
        return BaseHTTPError(
            eval(self.http_status),
            title=self.title,
            description=self.description,
            code=self.code,
        )


def _format_traceback():
    trace = traceback.format_exc().splitlines()

    traceback_dict = {"traceback": trace[1:]}

    for i in range(0, len(traceback_dict["traceback"])):
        traceback_dict["traceback"][i] = traceback_dict["traceback"][i].replace('"', "").strip()

    return traceback_dict


def request_error_handler(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except falcon.HTTPError as http_error:
            raise http_error
        except Exception as ex:
            raise BaseError(
                code="UCS000500",
                exception=ex
                # An internal error has occurred and its being investigated.
            ).http()

    return decorated
