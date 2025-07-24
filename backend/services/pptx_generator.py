from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
import os
from models import enums
import requests
from io import BytesIO

def build_pptx(presentation_id: int, title: str, slides: list, config: dict = None):
    prs = Presentation()
    
    for slide_data in slides:
        layout = slide_data.get("layout", "title")
        
        if layout == enums.SlideLayout.title.value:
            slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title slide
            slide.shapes.title.text = slide_data.get("title", "Title Slide")
            
        elif layout == enums.SlideLayout.bullet.value:
            slide = prs.slides.add_slide(prs.slide_layouts[1])  # Bullet slide
            slide.shapes.title.text = slide_data.get("title", "Bullets")
            body = slide.placeholders[1].text_frame
            for bullet in slide_data.get("bullets", []):
                p = body.add_paragraph()
                p.text = bullet
                p.level = 0
                
        elif layout == enums.SlideLayout.two_column.value:
            slide = prs.slides.add_slide(prs.slide_layouts[3])  # Section Header
            slide.shapes.title.text = slide_data.get("title", "Two Column")
            left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
            right_box = slide.shapes.add_textbox(Inches(5), Inches(1.5), Inches(4), Inches(4))
            left_frame = left_box.text_frame
            right_frame = right_box.text_frame
            left_frame.text = slide_data.get("left", "")
            right_frame.text = slide_data.get("right", "")
            
        elif layout == enums.SlideLayout.image.value:
            slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide
            slide.shapes.title.text = slide_data.get("title", "Image Slide")
            image_url = slide_data.get("image_url")
            
            if image_url:
                try:
                    # Download image
                    response = requests.get(image_url)
                    image_stream = BytesIO(response.content)
                    
                    # Add image to slide
                    slide.shapes.add_picture(
                        image_stream,
                        Inches(2), Inches(2),
                        width=Inches(6)
                    )
                except Exception as e:
                    print(f"Failed to add image: {str(e)}")
                    # Add placeholder rectangle if image fails
                    slide.shapes.add_shape(
                        MSO_SHAPE.RECTANGLE,
                        Inches(2), Inches(2),
                        Inches(6), Inches(4)
                    )
            else:
                # Add placeholder rectangle for placeholder URLs
                slide.shapes.add_shape(
                    MSO_SHAPE.RECTANGLE,
                    Inches(2), Inches(2),
                    Inches(6), Inches(4)
                )

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    path = os.path.abspath(f"./output/presentation_{presentation_id}.pptx")
    prs.save(path)
    return path