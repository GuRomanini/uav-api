import falcon
from falcon import Request, Response

from controllers import ServiceHelloWorldController

from utils.schema_handler import SchemaHandler

SERVICE_KEY_TO_CONTROLLER_MAPPER = {"15cf3b2c-7bf1-442a-97a5-9b744059bcfd": ServiceHelloWorldController}


class ServiceRequestResource:
    @SchemaHandler.validate("post_service_request.json")
    def on_post(self, req: Request, resp: Response):
        controller = SERVICE_KEY_TO_CONTROLLER_MAPPER[req.context.instance.media["service_key"]](
            context=req.context.instance
        )

        resp.media = controller.handle_request()
        resp.status = falcon.code_to_http_status(200)
