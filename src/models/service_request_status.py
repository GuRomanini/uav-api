from sqlalchemy import Column, Integer, String, DateTime
from models.base import Base


class ServiceRequestStatusModel(Base):
    __tablename__ = "ServiceRequestStatus"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    enumerator = Column(String)
    created_at = Column(DateTime, nullable=False, server_default="DEFAULT")
