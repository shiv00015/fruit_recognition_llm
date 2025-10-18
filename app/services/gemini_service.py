import google.generativeai as genai
from app.config import get_settings
import json
import re

class GeminiService:
    def __init__(self):
        settings = get_settings()
        api_key = settings.google_api_key
        print(f"Using API key: {api_key[:10]}...")  # Print first 10 chars for verification
        genai.configure(api_key=api_key)
        
        try:
            # Test connection and get model
            models = list(genai.list_models())
            print(f"Found {len(models)} models:")
            for m in models:
                print(f"- {m.name}")
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise

    async def analyze_image(self, image_data: bytes, prompt: str):
        try:
            print('prompt', prompt)
            response = self.model.generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            
            raw_text = response.text.strip()
            
            # Extract JSON part safely (handles ```json ... ``` format)
            match = re.search(r'\{[\s\S]*\}', raw_text)
            if match:
                json_str = match.group(0)
                try:
                    result = json.loads(json_str)
                except json.JSONDecodeError:
                    result = {"error": "Invalid JSON returned by model"}
            else:
                result = {"error": "No valid JSON found in model response"}
            
            
            return {"fruit_analysis": result}
        except Exception as e:
            import traceback
            error_details = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            print("Error details:", error_details)
            return error_details