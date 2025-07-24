from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
import os
from models import enums

def build_pptx(presentation_id: int, title: str, slides: list, config: dict = None):
    prs = Presentation()
    for slide_data in slides:
        layout = slide_data.get("layout", "title")
        slide = prs.slides.add_slide(prs.slide_layouts[0])

        if layout == enums.SlideLayout.title.value:
            slide.shapes.title.text = slide_data.get("title", "Title Slide")
        elif layout == enums.SlideLayout.bullet.value:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = slide_data.get("title", "Bullets")
            body = slide.shapes.placeholders[1].text_frame
            for bullet in slide_data.get("bullets", []):
                body.add_paragraph().text = bullet
        elif layout == enums.SlideLayout.two_column.value:
            slide.shapes.title.text = slide_data.get("title", "Two Column")
            left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
            right_box = slide.shapes.add_textbox(Inches(5), Inches(1.5), Inches(4), Inches(4))
            left_frame = left_box.text_frame
            right_frame = right_box.text_frame
            left_frame.text = slide_data.get("left", "")
            right_frame.text = slide_data.get("right", "")
        elif layout == enums.SlideLayout.image.value:
            slide.shapes.title.text = slide_data.get("title", "Image Slide")
            slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2), Inches(2), Inches(4), Inches(3))

    path = f"./output/presentation_{presentation_id}.pptx"
    os.makedirs("output", exist_ok=True)
    prs.save(path)
    return path