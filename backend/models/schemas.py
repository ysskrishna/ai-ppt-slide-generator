from pydantic import BaseModel, Field, field_validator
import re
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


ALLOWED_FONTS = {"Arial", "Calibri", "Times New Roman"}
HEX_COLOR_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")

class ConfigurationUpdate(BaseModel):
    font_name: Optional[str]
    font_color: Optional[str]
    background_color: Optional[str]

    @field_validator("font_name")
    def validate_font(cls, v):
        if v and v not in ALLOWED_FONTS:
            raise ValueError(f"Font '{v}' is not supported. Allowed fonts: {', '.join(ALLOWED_FONTS)}")
        return v

    @field_validator("font_color")
    def validate_font_color(cls, v):
        if v and not HEX_COLOR_REGEX.match(v):
            raise ValueError(f"Font color '{v}' is not a valid hex color (e.g., #RRGGBB)")
        return v

    @field_validator("background_color")
    def validate_background_color(cls, v):
        if v and not HEX_COLOR_REGEX.match(v):
            raise ValueError(f"Background color '{v}' is not a valid hex color (e.g., #RRGGBB)")
        return v

class PresentationOut(BaseModel):
    presentation_id: int
    topic: str
    content: List[SlideContent]
    configuration: Optional[Dict]

    class Config:
        orm_mode = True