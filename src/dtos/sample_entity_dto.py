from dtos.base import BaseDTO
from models import SampleEntity


class SampleEntityDTO(BaseDTO):
    def __init__(self, sample_entity: SampleEntity) -> None:

        self.sample_entity_key = sample_entity.sample_entity_key
        self.status = sample_entity.status.enumerator
