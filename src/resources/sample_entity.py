import falcon
from falcon import Request, Response

from controllers import SampleEntityController

from utils.schema_handler import SchemaHandler
from utils.security_tools import SecurityTools


class SampleEntityResource:
    @SchemaHandler.validate("post_sample_entity.json")
    def on_post(self, req: Request, resp: Response):
        requester_key = SecurityTools.validate_existent_selected_agent(req)
        sample_entity_controller = SampleEntityController(req.context.instance)
        sample_entity = sample_entity_controller.create_by_contract(requester_key, req.context.instance.media)

        resp.media = sample_entity
        resp.status = falcon.code_to_http_status(201)

    def on_get_by_key(self, req: Request, resp: Response, sample_entity_key: str):
        requester_key = SecurityTools.validate_existent_selected_agent(req)
        sample_entity_controller = SampleEntityController(req.context.instance)
        sample_entity = sample_entity_controller.get_by_key(requester_key, sample_entity_key)

        resp.media = sample_entity
        resp.status = falcon.code_to_http_status(200)

    @SchemaHandler.validate("patch_sample_entity.json")
    def on_patch_by_key(self, req: Request, resp: Response, sample_entity_key: str):
        requester_key = SecurityTools.validate_existent_selected_agent(req)
        sample_entity_controller = SampleEntityController(req.context.instance)
        sample_entity_controller.update_status(requester_key, sample_entity_key, req.context.instance.media)
        resp.status = falcon.code_to_http_status(202)

    def on_post_by_xml(self, req: Request, resp: Response):
        context = req.context.instance
        sample_entity_controller = SampleEntityController(context)

        sample_entity_xml = sample_entity_controller.create_xml(context.media)

        resp.media = sample_entity_xml
        resp.status = falcon.code_to_http_status(201)
