from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from models.enums import SlideLayout

class TitleSlide(BaseModel):
    layout: SlideLayout
    title: str

class BulletSlide(BaseModel):
    layout: SlideLayout
    title: str
    bullets: List[str]

class TwoColumnSlide(BaseModel):
    layout: SlideLayout
    title: str
    left: str
    right: str

class ImageSlide(BaseModel):
    layout: SlideLayout
    title: str
    image_url: str

SlideContent = Union[TitleSlide, BulletSlide, TwoColumnSlide, ImageSlide]

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
    topic: str
    content: List[SlideContent]
    configuration: Optional[Dict]

    class Config:
        orm_mode = True