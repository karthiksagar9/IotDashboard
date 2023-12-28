from sqlalchemy import Column, Integer, Float, String, DateTime
from database import Base
from datetime import datetime, timedelta

class SensorData(Base):
     __tablename__ = "sensor_data"
     id = Column(Integer, primary_key=True, index=True)
     device_name = Column(String)
     temperature = Column(Float)
     timestamp = Column(DateTime, default=datetime.utcnow)