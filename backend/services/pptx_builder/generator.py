from models import enums
from services.pptx_builder.slides.title import TitleSlideStrategy
from services.pptx_builder.slides.bullet import BulletSlideStrategy
from services.pptx_builder.slides.two_column import TwoColumnSlideStrategy
from services.pptx_builder.slides.image import ImageSlideStrategy


class SlideGenerator:
    def __init__(self):
        self.strategies = {
            enums.SlideLayout.title.value: TitleSlideStrategy(),
            enums.SlideLayout.bullet.value: BulletSlideStrategy(),
            enums.SlideLayout.two_column.value: TwoColumnSlideStrategy(),
            enums.SlideLayout.image.value: ImageSlideStrategy(),
        }

    def add_slide(self, prs, slide_data, config, **kwargs):
        layout = slide_data.get("layout", enums.SlideLayout.title.value)
        strategy = self.strategies.get(layout)
        if not strategy:
            raise ValueError(f"No strategy for layout: {layout}")
        return strategy.add_slide(prs, slide_data, config, **kwargs)