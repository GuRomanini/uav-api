import xmltodict as XMLToDict

from controllers.base_controller import BaseController
from dtos.sample_entity_dto import SampleEntityDTO
from dtos.sample_xml_dto import SampleXmlDTO
from repositories import SampleEntityRepository
from models import SampleEntity
from utils.context import Context
from errors import NotFoundSampleEntity, SampleEntityFinalStatus


class SampleEntityController(BaseController):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__)
        self.sample_entity_repository = SampleEntityRepository(context)

    def create_by_contract(self, requester_key: str, sample_entity_json: dict) -> SampleEntity:
        self.logger.debug("Creating a new Sample Entity")
        sample_entity = self.sample_entity_repository.create(
            requester_key=requester_key,
            sample_entity_data=sample_entity_json.get("hello"),
        )
        self.context.db_session.commit()

        sample_entity_dto = SampleEntityDTO(sample_entity).to_dict()

        return sample_entity_dto

    def create_xml(self, sample_entity_schema: str):
        self.logger.debug(f"Creating a new Sample XML of {sample_entity_schema}")

        xml_sample_entity = XMLToDict.parse(sample_entity_schema)

        sample_entity_xml = self.sample_entity_repository.create_xml(xml_data=xml_sample_entity)

        self.sample_entity_repository.commit()

        sample_entity_xml_dto = SampleXmlDTO(sample_entity_xml).to_dict()

        return sample_entity_xml_dto

    def get_by_key(self, requester_key: str, sample_entity_key: str) -> SampleEntity:
        self.logger.debug(f"Fetching Entity with key {sample_entity_key} for requester {requester_key}")
        sample_entity = self.sample_entity_repository.get_by_requester_and_key(requester_key, sample_entity_key)
        if sample_entity is None:
            raise NotFoundSampleEntity(sample_entity_key)

        sample_entity_dto = SampleEntityDTO(sample_entity).to_dict()

        return sample_entity_dto

    def update_status(self, requester_key: str, sample_entity_key: str, update_payload: dict) -> None:
        self.logger.debug(f"Fetching Entity with key {sample_entity_key} for requester {requester_key}")
        sample_entity = self.sample_entity_repository.get_by_requester_and_key(requester_key, sample_entity_key)
        if sample_entity is None:
            raise NotFoundSampleEntity(sample_entity_key)

        old_status = sample_entity.status.enumerator
        new_status = update_payload["status"]

        if old_status != "created":
            raise SampleEntityFinalStatus(old_status, new_status)

        self.sample_entity_repository.update_status(sample_entity, new_status)
