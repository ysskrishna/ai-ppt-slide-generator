from pptx import Presentation
import os
from services.pptx_builder.generator import SlideGenerator

def build_pptx(presentation_id: int, slides: list, config: dict, **kwargs):
    prs = Presentation()
    generator = SlideGenerator()
    for slide_data in slides:
        generator.add_slide(prs, slide_data, config, **kwargs)
    os.makedirs("storage", exist_ok=True)
    path = os.path.abspath(f"./storage/presentation_{presentation_id}.pptx")
    prs.save(path)
    return path