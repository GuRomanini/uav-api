from sqlalchemy import Column, Integer, String
from models.base import Base


class SampleEntityStatus(Base):
    __tablename__ = "SampleEntityStatus"
    __table_args__ = {"schema": "service_handler"}

    id = Column(Integer, primary_key=True)
    enumerator = Column(String)
