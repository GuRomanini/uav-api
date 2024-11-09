import falcon
from falcon import Request, Response

from controllers import ServiceHelloWorldController

from utils.schema_handler import SchemaHandler

SERVICE_KEY_TO_CONTROLLER_MAPPER = {
    "b580fdc5-ff9d-4d2a-bd97-49b5b5448822": ServiceHelloWorldController
}

class ServiceRequestResource:
    @SchemaHandler.validate("post_service_request.json")
    def on_post(self, req: Request, resp: Response):
        controller = SERVICE_KEY_TO_CONTROLLER_MAPPER[req.context.instance.media["service_key"]](context=req.context.instance)

        resp.media = controller.handle_request()
        resp.status = falcon.code_to_http_status(200)
