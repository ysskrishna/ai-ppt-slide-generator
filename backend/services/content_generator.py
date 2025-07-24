import google.generativeai as genai
import json
import re
from core.config import Config
from models import enums

genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_content_with_gemini(topic: str, num_slides: int):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Generate a presentation with {num_slides} slides on the topic: '{topic}'. "
        f"Format each slide exactly according to these structures based on layout type. "
        f"Include ONLY the fields specified for each type:\n\n"
        f"1. For title slides ({enums.SlideLayout.title.value}):\n"
        f"   {{\n"
        f"     'layout': 'title',\n"
        f"     'title': 'Main title here'\n"
        f"   }}\n\n"
        f"2. For bullet slides ({enums.SlideLayout.bullet.value}):\n"
        f"   {{\n"
        f"     'layout': 'bullet',\n"
        f"     'title': 'Slide title here',\n"
        f"     'bullets': ['Point 1', 'Point 2', 'Point 3']\n"
        f"   }}\n\n"
        f"3. For two-column slides ({enums.SlideLayout.two_column.value}):\n"
        f"   {{\n"
        f"     'layout': 'two_column',\n"
        f"     'title': 'Slide title here',\n"
        f"     'left': 'Left column content here',\n"
        f"     'right': 'Right column content here'\n"
        f"   }}\n\n"
        f"4. For image slides ({enums.SlideLayout.image.value}):\n"
        f"   {{\n"
        f"     'layout': 'image',\n"
        f"     'title': 'Slide title here',\n"
        f"     'image_url': 'URL or placeholder for image'\n"
        f"   }}\n\n"
        f"IMPORTANT: For each slide type, include ONLY the fields shown in the example. "
        f"Do not add any extra fields. Each layout type must match its structure exactly.\n\n"
        f"Return the response as a JSON array of slides following these exact structures. "
        f"For image slides, you can use placeholder text for image_url."
    )
    try:
        response = model.generate_content(prompt)
        json_data = response.text
        json_clean = re.sub(r"```json|```", "", json_data).strip()
        slides = json.loads(json_clean)
        return slides
    except Exception as e:
        print("Gemini content generation failed:", e)
        raise RuntimeError("Gemini content generation failed")