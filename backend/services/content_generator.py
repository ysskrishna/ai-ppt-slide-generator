import google.generativeai as genai
import json
import re
from core.config import Config
from models import enums

genai.configure(api_key=Config.GEMINI_API_KEY)

def generate_content_with_gemini(topic: str, num_slides: int = 5):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Generate a presentation with {num_slides} slides on the topic: '{topic}'. "
        f"Each slide should include:\n"
        f"- layout type ({enums.SlideLayout.title.value}, {enums.SlideLayout.bullet.value}, {enums.SlideLayout.two_column.value}, {enums.SlideLayout.image.value})\n"
        f"- title\n"
        f"- content (bullets or paragraph or 2-column text)\n"
        f"Return the response in JSON format as a list of slides."
    )
    try:
        response = model.generate_content(prompt)
        json_data = response.text
        json_clean = re.sub(r"```json|```", "", json_data).strip()
        slides = json.loads(json_clean)
        citations = f"Content generated using Google Gemini for topic '{topic}'."
        return slides, citations
    except Exception as e:
        print("Gemini content generation failed:", e)
        raise RuntimeError("Gemini content generation failed")