from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
import os
from models import enums
import requests
from io import BytesIO

def build_pptx(presentation_id: int, slides: list, config: dict = None):
    prs = Presentation()
    
    for slide_data in slides:
        layout = slide_data.get("layout", "title")
        
        if layout == enums.SlideLayout.title.value:
            slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title slide
            slide.shapes.title.text = slide_data.get("title", "")
            
        elif layout == enums.SlideLayout.bullet.value:
            slide = prs.slides.add_slide(prs.slide_layouts[1])  # Bullet slide
            slide.shapes.title.text = slide_data.get("title","")
            body = slide.placeholders[1].text_frame
            for bullet in slide_data.get("bullets", []):
                p = body.add_paragraph()
                p.text = bullet
                p.level = 0
                
        elif layout == enums.SlideLayout.two_column.value:
            slide = prs.slides.add_slide(prs.slide_layouts[3])  # Use default two-content layout
            slide.shapes.title.text = slide_data.get("title", "")

            # Get the content placeholders (usually index 1 and 2)
            left_placeholder = slide.placeholders[1]
            right_placeholder = slide.placeholders[2]

            # Clear existing content
            left_placeholder.text = ""
            right_placeholder.text = ""

            # Add left content
            for para in slide_data.get("left", "").split("\n"):
                p = left_placeholder.text_frame.add_paragraph()
                p.text = para.strip()
                p.level = 0

            # Add right content
            for para in slide_data.get("right", "").split("\n"):
                p = right_placeholder.text_frame.add_paragraph()
                p.text = para.strip()
                p.level = 0
            
        elif layout == enums.SlideLayout.image.value:
            slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide
            slide.shapes.title.text = slide_data.get("title","")
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
                print(f"No image URL provided for slide: {slide_data.get('title')}")
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