import falcon
from falcon import Request, Response

from controllers import ServiceController
from utils.schema_handler import SchemaHandler


class ServiceResource:
    @SchemaHandler.validate("post_service.json")
    def on_post(self, req: Request, resp: Response):
        service_controller = ServiceController(req.context.instance)
        response = service_controller.register_service(service_data=req.context.instance.media)

        resp.media = response
        resp.status = falcon.code_to_http_status(201)
