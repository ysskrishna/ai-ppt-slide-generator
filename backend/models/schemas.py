from pydantic import BaseModel
from typing import Optional, List, Dict
from models import enums

class SlideContent(BaseModel):
    layout: enums.SlideLayout
    title: Optional[str]
    body: Optional[str]
    bullets: Optional[List[str]]
    left: Optional[str]
    right: Optional[str]
    image_url: Optional[str]

class PresentationCreate(BaseModel):
    topic: str
    custom_content: Optional[List[SlideContent]] = None

class ConfigurationUpdate(BaseModel):
    num_slides: Optional[int] = 5
    theme: Optional[str]
    font: Optional[str]
    color: Optional[str]

class PresentationOut(BaseModel):
    presentation_id: int
    title: str
    topic: str
    content: List[SlideContent]
    configuration: Optional[Dict]
    citations: Optional[str]

    class Config:
        orm_mode = True