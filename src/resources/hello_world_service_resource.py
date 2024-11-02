import falcon
from falcon import Request, Response

from utils.schema_handler import SchemaHandler


class HelloWorldServiceResource:
    @SchemaHandler.validate("post_hello_world_service.json")
    def on_post(self, req: Request, resp: Response):
        resp.media = {"message": "Hello world!"}
        resp.status = falcon.code_to_http_status(200)
