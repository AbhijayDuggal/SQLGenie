import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiLLM:
    def __init__(self, model_name=None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        genai.configure(api_key=api_key)

        # Use model_name if provided; default to stable flash model
        self.model_name = model_name or "models/gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
