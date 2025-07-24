from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, declarative_mixin
import datetime
from core.dbutils import Base


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

# Presentation model
class Presentation(Timestamp, Base):
    __tablename__ = "presentations"
    presentation_id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    config = Column(JSON, nullable=True)  # Stores slide configuration, fonts, colors, etc.
    slides = relationship("Slide", back_populates="presentation", cascade="all, delete-orphan")

# Slide model
class Slide(Timestamp, Base):
    __tablename__ = "slides"
    slide_id = Column(Integer, primary_key=True, index=True)
    presentation_id = Column(Integer, ForeignKey("presentations.presentation_id"), nullable=False)
    type = Column(String, nullable=False)  # e.g., title, bullet, two-column, image
    content = Column(JSON, nullable=True)  # Content as JSON (text, bullets, etc.)
    image_url = Column(String, nullable=True)
    citation = Column(Text, nullable=True)
    presentation = relationship("Presentation", back_populates="slides")
