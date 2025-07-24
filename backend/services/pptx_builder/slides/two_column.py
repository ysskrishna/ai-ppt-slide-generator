from services.pptx_builder.utils import set_slide_title_and_style

class TwoColumnSlideStrategy:
    def add_slide(self, prs, slide_data, config, **kwargs):
        slide = prs.slides.add_slide(prs.slide_layouts[3])
        set_slide_title_and_style(slide, slide_data, config.get("background_color", "#FFFFFF"), config.get("font_name", "Arial"), config.get("font_color", "#000000"))
        left_placeholder = slide.placeholders[1]
        right_placeholder = slide.placeholders[2]
        left_placeholder.text = ""
        right_placeholder.text = ""
        for para in slide_data.get("left", "").split("\n"):
            p = left_placeholder.text_frame.add_paragraph()
            p.text = para.strip()
            p.level = 0
        for para in slide_data.get("right", "").split("\n"):
            p = right_placeholder.text_frame.add_paragraph()
            p.text = para.strip()
            p.level = 0
        return slide 