from fastapi import APIRouter, UploadFile, File
from app.services.gemini_service import GeminiService
from typing import Optional

router = APIRouter()
gemini_service = GeminiService()


prompt = """
You are an expert fruit recognition and nutrition analysis model.

Your task:
- Analyze the given image input.
- Detect and identify only fruits (ignore any non-fruit objects).
- For each fruit detected, provide the following detailed information in structured JSON format.

Respond strictly in a valid JSON (Python dictionary) format.
Do not include any explanations, comments, or text outside this format.

Example output format:
{
  "banana": {
    "name_of_fruit": "Banana",
    "quantity_detected": "3",
    "freshness_status": "Ripe",
    "confidence_score": "97%",
    "color_analysis": "Bright yellow with small brown spots",
    "shape_description": "Curved cylindrical",
    "taste_profile": "Sweet and soft texture",
    "calories_per_100g": "89 kcal",
    "carbohydrates": "22.8 g",
    "fiber": "2.6 g",
    "vitamins": ["Vitamin B6", "Vitamin C"],
    "benefits_for_human_body": "Supports digestion, boosts energy, helps heart health",
    "nutritional_value_summary": "High in potassium and fiber, low in fat",
    "storage_tips": "Store at room temperature until ripe, then refrigerate",
    "region_and_season": "Tropical regions, summer season"
  }
}

Instructions:
1. If multiple fruits are present, include each as a separate key within the JSON object.
2. If no fruit is detected, return an empty JSON object: {}
3. Always include all fields for each fruit:
   - name_of_fruit
   - quantity_detected
   - freshness_status
   - confidence_score
   - color_analysis
   - shape_description
   - taste_profile
   - calories_per_100g
   - carbohydrates
   - fiber
   - vitamins
   - benefits_for_human_body
   - nutritional_value_summary
   - storage_tips
   - region_and_season
4. Keep keys lowercase and values concise and accurate.
5. For “freshness_status”, use one of: ["Fresh", "Rotten", "Ripe", "Unripe"].
6. When using a webcam or camera scan, assume natural lighting and analyze as realistically as possible.
7. Output must be valid JSON that can be directly parsed by Python’s `json.loads()`.
"""


@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...), prompt: Optional[str] = prompt):
    image_data = await file.read()
    print("-----------called")
    result = await gemini_service.analyze_image(image_data, prompt)
    return result
