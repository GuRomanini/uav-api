from sqlalchemy import Column, Integer, DateTime, JSON
from models.base import Base


class SampleXml(Base):
    __tablename__ = "SampleXml"
    __table_args__ = {"schema": "base"}

    id = Column(Integer, primary_key=True)
    xml_data = Column(JSON)

    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")
