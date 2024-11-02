import falcon
import os
from uuid import uuid4

from connectors import ServiceHandlerConnector

from utils.context import Context
from utils.logger import LogHandler
from utils.xml_handler import XMLHandler
from errors import APIErrorHandler, BaseException, error_verification

from middlewares.context_creator import ContextCreator
from middlewares.input_output import InputOutputMiddleware
from middlewares.secure_headers import SecureHeaders

from resources import (
    HealthcheckResource,
    HelloWorldServiceResource,
    Home,
    ServiceResource,
    SinkResource,
    TimeResource,
)

from constants import check_variables


def create():
    api = falcon.App(
        middleware=[
            ContextCreator(),
            InputOutputMiddleware(),
            SecureHeaders(),
        ]
    )

    handlers = falcon.media.Handlers({falcon.MEDIA_XML: XMLHandler()})

    api.req_options.media_handlers = handlers

    home_resource = Home()
    api.add_route("/", home_resource)
    hc_resource = HealthcheckResource()
    api.add_route("/health_check", hc_resource)

    sink_resource = SinkResource()
    api.add_sink(sink_resource, r"/")

    time_resource = TimeResource()
    api.add_route("/time", time_resource)

    service_resource = ServiceResource()
    api.add_route("/service", service_resource)

    hello_world_service_resource = HelloWorldServiceResource()
    api.add_route("/service/hello_world", hello_world_service_resource)

    return api


def main():
    error_verification()
    check_variables()
    LogHandler()
    api = create()

    api.add_error_handler(Exception, APIErrorHandler.unexpected)
    api.add_error_handler(falcon.HTTPMethodNotAllowed, APIErrorHandler.method_not_allowed)
    api.add_error_handler(BaseException, APIErrorHandler.uaas_exception)

    service_handler_connector = ServiceHandlerConnector(context=Context(global_trace_id=str(uuid4())))
    response = service_handler_connector.register_uav(uav_name="Sample UAV")
    os.environ["UAV_KEY"] = response["uav_key"]

    return api


application = main()
