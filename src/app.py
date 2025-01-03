import falcon

from utils.logger import LogHandler
from utils.xml_handler import XMLHandler
from errors import APIErrorHandler, BaseException, error_verification

from middlewares.context_creator import ContextCreator
from middlewares.input_output import InputOutputMiddleware

from resources import (
    HealthcheckResource,
    Home,
    ServiceRequestResource,
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

    service_request_resource = ServiceRequestResource()
    api.add_route("/service_request/request", service_request_resource)

    return api


def main():
    error_verification()
    check_variables()
    LogHandler()
    api = create()

    api.add_error_handler(Exception, APIErrorHandler.unexpected)
    api.add_error_handler(falcon.HTTPMethodNotAllowed, APIErrorHandler.method_not_allowed)
    api.add_error_handler(BaseException, APIErrorHandler.uaas_exception)

    return api


application = main()
