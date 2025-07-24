from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from core.dbutils import Base
from sqlalchemy.orm import declarative_mixin
from datetime import datetime

@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

# Presentation model
class Presentation(Timestamp, Base):
    __tablename__ = "presentations"

    presentation_id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String)
    content = Column(JSON)
    configuration = Column(JSON, nullable=True)
    pptx_path = Column(String, nullable=True)

