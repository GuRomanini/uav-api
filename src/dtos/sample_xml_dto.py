from dtos.base import BaseDTO
from models import SampleXml


class SampleXmlDTO(BaseDTO):
    def __init__(self, sample_xml: SampleXml) -> None:
        self.xml_data = sample_xml.xml_data
