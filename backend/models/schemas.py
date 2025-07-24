from pydantic import BaseModel, Field
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
    num_slides: Optional[int] = Field(
        default=5, ge=1, le=20, description="Number of slides (min 1, max 20)"
    )

    custom_content: Optional[List[SlideContent]] = None

class ConfigurationUpdate(BaseModel):
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