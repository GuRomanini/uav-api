from repositories.base_repository import BaseRepository
from utils.context import Context
from models import SampleEntity, SampleEntityStatus, SampleEntityStatusEvent, SampleXml
from uuid import uuid4
from datetime import datetime


class ServiceRequestRepository(BaseRepository):
    def __init__(self, context: Context) -> None:
        super().__init__(context=context, class_name=__name__)

    def create(
        self,
        requester_key: str,
        sample_entity_data: str,
    ) -> SampleEntity:
        sample_entity = SampleEntity()
        sample_entity.requester_key = requester_key
        sample_entity.sample_entity_data = sample_entity_data
        sample_entity.sample_entity_key = str(uuid4())
        sample_entity.status = self.get_enumerator(SampleEntityStatus, "created")

        self.add(sample_entity)
        return sample_entity

    def create_xml(
        self,
        xml_data: dict,
    ) -> SampleXml:
        sample_entity = SampleXml()
        sample_entity.xml_data = str(xml_data)

        self.add(sample_entity)
        return sample_entity

    def update_status(self, sample_entity: SampleEntity, new_status_enumerator: str) -> None:
        new_status = self.get_enumerator(SampleEntityStatus, new_status_enumerator)
        sample_entity.status = new_status

        new_status_event = SampleEntityStatusEvent()
        new_status_event.status = new_status
        new_status_event.event_date = datetime.utcnow()

        sample_entity.status_events.append(new_status_event)

    def get_by_requester_and_key(self, requester_key: str, sample_entity_key: str) -> SampleEntity:
        sample_entity = (
            self.query(SampleEntity)
            .filter(SampleEntity.requester_key == requester_key)
            .filter(SampleEntity.sample_entity_key == sample_entity_key)
            .first()
        )
        return sample_entity
