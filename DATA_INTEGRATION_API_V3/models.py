from sqlalchemy import Column, Integer, String, Float
from database import Base

class DataReading(Base):
    __tablename__ = 'data_readings'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Integer, index=True)
    metric_name = Column(String, index=True)
    metric_value = Column(Float)
