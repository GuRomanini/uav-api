from controllers.base_controller import BaseController
from mappers import ServiceMapper
from repositories import ServiceRepository
from models import ServiceModel
from utils.context import Context

class ServiceController(BaseController):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__)
        self.service_repository = ServiceRepository(context)

    def create_by_data(self, service_data: dict) -> dict:
        self.logger.debug("Creating a new Service")
        service = self.service_repository.create(service_data)
        self.context.db_session.commit()

        return ServiceMapper.to_dto(service)

    # def get_by_key(self, requester_key: str, sample_entity_key: str) -> SampleEntity:
    #     self.logger.debug(f"Fetching Entity with key {sample_entity_key} for requester {requester_key}")
    #     sample_entity = self.sample_entity_repository.get_by_requester_and_key(requester_key, sample_entity_key)
    #     if sample_entity is None:
    #         raise NotFoundSampleEntity(sample_entity_key)

    #     sample_entity_dto = SampleEntityDTO(sample_entity).to_dict()

    #     return sample_entity_dto

    # def update_status(self, requester_key: str, sample_entity_key: str, update_payload: dict) -> None:
    #     self.logger.debug(f"Fetching Entity with key {sample_entity_key} for requester {requester_key}")
    #     sample_entity = self.sample_entity_repository.get_by_requester_and_key(requester_key, sample_entity_key)
    #     if sample_entity is None:
    #         raise NotFoundSampleEntity(sample_entity_key)

    #     old_status = sample_entity.status.enumerator
    #     new_status = update_payload["status"]

    #     if old_status != "created":
    #         raise SampleEntityFinalStatus(old_status, new_status)

    #     self.sample_entity_repository.update_status(sample_entity, new_status)
