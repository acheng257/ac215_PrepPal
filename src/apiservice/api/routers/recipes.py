from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.llm_rag_utils import generate_recommendation_list
from models.database import get_db
from models.user_history import UserHistory
from sqlalchemy.future import select
from uuid import UUID as PythonUUID
import uuid
import logging

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.post("/get_recs")
async def get_recs(body: dict, db: AsyncSession = Depends(get_db)):
    try:
        # Extract and log request data
        cooking_time = body["cookingTime"]
        serving_size = body["servings"]
        cuisine = body["cuisine"]
        ingredients_query = ", ".join(body["ingredients"])
        logger.debug(f"Received request - Cooking Time: {cooking_time}, Serving Size: {serving_size}, Cuisine: {cuisine}, Ingredients: {ingredients_query}")

        # Generate recommendations
        content_dict = {"ingredients": ingredients_query, "pantry": "sugar, pepper, broccoli, penne pasta, tomatoes, potatoes, flour"}
        recommendations = generate_recommendation_list(content_dict)

        rankings = recommendations["ranking"]
        list_of_recipes = recommendations["possible_recipes"]

        # Parse recipes
        recipes_dicts = []
        for recipe in list_of_recipes.split("Recipe: ")[1:]:
            try:
                title, recipe = recipe.split("\nRecipe Servings: ")
                servings, recipe = recipe.split("\nTotal Time: ")
                time, recipe = recipe.split("\nIngredients: ")
                ingredients, recipe = recipe.split("\nCalories: ")
                calories, recipe = recipe.split("\nSugar")
                _, instructions = recipe.split("\nInstructions: ")
                instructions = instructions.split("\n")[:-1]

                recipe_dict = {
                    "title": title.strip(),
                    "time": time.strip(),
                    "servings": servings.strip(),
                    "ingredients": [ing.strip() for ing in ingredients.split(", ")],
                    "calories": calories.strip(),
                    "instructions": [instr.strip() for instr in instructions],
                }
                recipes_dicts.append(recipe_dict)
            except ValueError as ve:
                logger.error(f"Error parsing recipe: {ve}")
                continue

        logger.debug(f"Rankings: {rankings}")

        # Parse rankings
        try:
            rankings = rankings.split("Rank 1: ")[-1]
            rank1, rankings = rankings.split("Rank 2: ")
            rank2, rankings = rankings.split("Rank 3: ")
            rank3, rankings = rankings.split("Rank 4: ")
            rank4, rank5 = rankings.split("Rank 5: ")

            all_rankings = [rank1, rank2, rank3, rank4, rank5]
            all_rankings = [ranking.split("\n") for ranking in all_rankings]
            all_rankings[-1] = all_rankings[-1][:-2]
        except ValueError as ve:
            logger.error(f"Error parsing rankings: {ve}")
            raise HTTPException(status_code=500, detail="Error processing rankings")

        # Order recipes based on rankings
        ordered_recipe_dicts = []
        for ranking in all_rankings:
            try:
                current_ranking_title, missing_ingredients = ranking
                for recipe_dict in recipes_dicts:
                    if recipe_dict["title"] == current_ranking_title:
                        recipe_dict["missing_ingredients"] = missing_ingredients.split("Here are the ingredients you still need: ")[-1].strip().split(", ")
                        ordered_recipe_dicts.append(recipe_dict)
                        break
            except ValueError as ve:
                logger.error(f"Error processing ranking entry: {ve}")
                continue

        # Generate recommendation data
        recommendation_id = uuid.uuid4()
        recommendation_data = {"cooking_time": cooking_time, "serving_size": serving_size, "cuisine": cuisine, "ingredients": body["ingredients"], "recommendations": ordered_recipe_dicts}

        # Parse user_id
        user_id = PythonUUID(body["userId"])
        print("user_id is", user_id)

        # Check if UserHistory exists
        existing_history_result = await db.execute(select(UserHistory).where(UserHistory.user_id == user_id))
        existing_history = existing_history_result.scalar_one_or_none()

        if existing_history:
            # Update existing UserHistory
            logger.debug(f"Updating existing UserHistory for user_id: {user_id}")
            existing_history.user_id = user_id
            existing_history.details = {"recommendation_id": str(recommendation_id)}
            existing_history.recommendation_id = recommendation_id
            existing_history.recommendation_data = recommendation_data
        else:
            # Create new UserHistory
            logger.debug(f"Creating new UserHistory for user_id: {user_id}")
            user_history = UserHistory(user_id=user_id, details={"recommendation_id": str(recommendation_id)}, recommendation_id=recommendation_id, recommendation_data=recommendation_data)
            db.add(user_history)

        # Commit the transaction
        try:
            await db.commit()
            logger.info(f"User history {'updated' if existing_history else 'added'} successfully for user_id: {user_id}")
        except Exception as commit_error:
            await db.rollback()
            logger.error(f"Error committing transaction: {commit_error}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")

        return {"recommendations": ordered_recipe_dicts, "recommendation_id": str(recommendation_id)}

    except Exception as e:
        logger.error(f"An unexpected error occurred in get_recs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
