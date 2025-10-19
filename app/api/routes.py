from fastapi import APIRouter, UploadFile, File
from app.services.gemini_service import GeminiService
from typing import Optional

router = APIRouter()
gemini_service = GeminiService()


prompt = """
You are an expert fruit recognition and nutrition analysis model.

Your task:
- Analyze the given image.
- Identify only fruits (ignore any non-fruit objects).
- For each fruit detected, provide detailed nutritional information.

Respond strictly in a valid JSON (Python dictionary) format as shown below.
Do not include any explanations or text outside of this format.

Example output format:
"banana" : {
  "name_of_fruit": "Banana",
  "calories_per_100g": "89 kcal",
  "carbohydrates": "22.8 g",
  "fiber": "2.6 g",
  "vitamins": ["Vitamin B6", "Vitamin C"],
  "benefits_for_human_body": "Helps digestion, provides instant energy, supports heart health"
}

Instructions:
- If no fruit is detected, return an empty JSON object: {}
- Always use lowercase keys exactly as shown.
- please make sure all keys name_of_fruit, calories_per_100g, carbohydrates, fiber, vitamins, benefits_for_human_body should available in (Python dictionary) as mentioned in the example
- Be concise and accurate in your nutrient values and benefits.
- make sure all fruits or single fruit should contain inside (python dictionary) as mentioned in the example
"""

@router.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: Optional[str] = prompt
):
    image_data = await file.read()
    print("-----------called")
    result = await gemini_service.analyze_image(image_data, prompt)
    return result