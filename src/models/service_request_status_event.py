from sqlalchemy import Column, ForeignKey, Integer, DateTime
from models.base import Base
from sqlalchemy.orm import relationship
from models import ServiceRequestModel, ServiceRequestStatusModel


class ServiceRequestStatusEventModel(Base):
    __tablename__ = "ServiceRequestStatusEvent"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    service_request_id = Column(Integer, ForeignKey(ServiceRequestModel.id))
    service_request_status_id = Column(Integer, ForeignKey(ServiceRequestStatusModel.id))
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")

    service_request = relationship(
        "ServiceRequest",
        foreign_keys=[service_request_id],
        back_populates="status_events",
        lazy="joined",
    )
    service_request_status = relationship(
        "ServiceRequestStatus", foreign_keys=[service_request_status_id], lazy="joined"
    )
