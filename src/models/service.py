from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base
from models import SampleEntityStatus


class ServiceModel(Base):
    __tablename__ = "Service"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    service_key = Column(String)
    service_type_id = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")

    service_type = relationship(
        "ServiceTypeModel", foreign_keys=[service_type_id], lazy="joined"
    )

