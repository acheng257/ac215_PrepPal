from fastapi import APIRouter
from api.utils.llm_rag_utils import generate_recommendation_list

router = APIRouter()


@router.post("/get_recs")
async def get_recs(body: dict):
    print("BODY", body)
    data = body["filters"]
    # cooking_time = data["cookingTime"]
    # serving_size = data["servings"]
    # cuisine = data["cuisine"]
    ingredients_query = ", ".join(data["ingredients"])
    # more_recommendations = body["more_recommendations"]

    content_dict = {"ingredients": ingredients_query, "pantry": "sugar, pepper, broccoli, penne pasta, tomatoes, potatoes, flour"}

    recommendations = generate_recommendation_list(content_dict)

    return {"recommendations": recommendations}
