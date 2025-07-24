from services.pptx_builder.utils import set_slide_title_and_style

class BulletSlideStrategy:
    def add_slide(self, prs, slide_data, config, **kwargs):
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        set_slide_title_and_style(slide, slide_data, config.get("background_color", "#FFFFFF"), config.get("font_name", "Arial"), config.get("font_color", "#000000"))
        body = slide.placeholders[1].text_frame
        for bullet in slide_data.get("bullets", []):
            p = body.add_paragraph()
            p.text = bullet
            p.level = 0
        return slide 