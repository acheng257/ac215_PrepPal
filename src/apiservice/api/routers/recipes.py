from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.llm_rag_utils import generate_recommendation_list
from models.database import get_db
from models.user_history import UserHistory
from models.users import User, UserPreferences
from sqlalchemy.future import select
from uuid import UUID as PythonUUID
import uuid
import logging
from models.recipes import Recipes
from sqlalchemy import func
from sqlalchemy.orm import joinedload

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_recipe(text: str) -> dict:
    """
    Parses the recipe text and extracts details.
    Expected format:

    Title: Recipe Title
    Ingredients:
    • Ingredient 1
    • Ingredient 2
    Instructions:
    Step 1.
    Step 2.
    Cooking Time: 45 minutes
    Calories: 600
    Protein: 25
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    recipe = {"title": "", "ingredients": [], "instructions": "", "cooking_time": 0, "calories": 0, "protein": 0}

    current_section = None

    for line in lines:
        if line.startswith("Title:"):
            recipe["title"] = line.replace("Title:", "").strip()
        elif line.startswith("Ingredients:"):
            current_section = "ingredients"
        elif line.startswith("Instructions:"):
            current_section = "instructions"
        elif line.startswith("Cooking Time:"):
            time_str = line.replace("Cooking Time:", "").replace("minutes", "").strip()
            try:
                recipe["cooking_time"] = int(time_str)
            except ValueError:
                recipe["cooking_time"] = 0
        elif line.startswith("Calories:"):
            calories_str = line.replace("Calories:", "").strip()
            try:
                recipe["calories"] = int(calories_str)
            except ValueError:
                recipe["calories"] = 0
        elif line.startswith("Protein:"):
            protein_str = line.replace("Protein:", "").strip()
            try:
                recipe["protein"] = int(protein_str)
            except ValueError:
                recipe["protein"] = 0
        else:
            if current_section == "ingredients":
                # Remove bullet points like '•' or '-' and trim
                ingredient = line.lstrip("•- ").strip()
                if ingredient:
                    recipe["ingredients"].append(ingredient)
            elif current_section == "instructions":
                recipe["instructions"] += line + " "

    # Trim the instructions
    recipe["instructions"] = recipe["instructions"].strip()

    return recipe


@router.post("/get_recs")
async def get_recs(body: dict, db: AsyncSession = Depends(get_db)):
    try:
        # Extract and log request data
        cooking_time = body["cookingTime"]
        serving_size = body["servings"]
        cuisine = body["cuisine"]
        ingredients_query = ", ".join(body["ingredients"])
        user_id = body["userId"]
        logger.debug(f"Received request - Cooking Time: {cooking_time}, Serving Size: {serving_size}, Cuisine: {cuisine}, Ingredients: {ingredients_query}")

        # Query database for pantry items for user
        query = select(User).options(joinedload(User.pantry_items)).where(User.user_id == user_id)
        result = await db.execute(query)
        user = result.unique().scalar_one_or_none()

        pantry_string = ""
        if user and user.pantry_items:
            # Assuming the first (and only) pantry item contains the JSON of items
            pantry_json = user.pantry_items[0].items
            pantry_items = list(pantry_json.keys())
            pantry_string = ", ".join(pantry_items)

        # Generate recommendations
        content_dict = {"ingredients": ingredients_query, "pantry": pantry_string}
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


@router.post("/upload-recipe")
async def upload_recipe(recipeFile: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not recipeFile.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")

    content = await recipeFile.read()
    recipe_data = parse_recipe_file(content.decode())

    try:
        # Check if recipe with same title exists
        existing_recipe = await db.execute(select(Recipes).where(Recipes.title == recipe_data["title"]))
        existing_recipe = existing_recipe.scalar_one_or_none()

        if existing_recipe:
            # Update existing recipe
            existing_recipe.instructions = recipe_data["instructions"]
            existing_recipe.ingredients = recipe_data["ingredients"]
            existing_recipe.cooking_time = recipe_data["cooking_time"]
            existing_recipe.calories = recipe_data["calories"]
            existing_recipe.protein = recipe_data["protein"]
            await db.commit()
            return {"success": True, "message": "Recipe updated successfully", "recipe_id": str(existing_recipe.recipe_id)}

        # Create new recipe if it doesn't exist
        new_recipe = Recipes(
            recipe_id=uuid.uuid4(),
            title=recipe_data["title"],
            instructions=recipe_data["instructions"],
            ingredients=recipe_data["ingredients"],
            cooking_time=recipe_data["cooking_time"],
            calories=recipe_data["calories"],
            protein=recipe_data["protein"],
        )
        db.add(new_recipe)
        await db.commit()
        await db.refresh(new_recipe)
        return {"success": True, "message": "Recipe uploaded successfully", "recipe_id": str(new_recipe.recipe_id)}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error uploading recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def parse_recipe_file(content: str) -> dict:
    lines = content.split("\n")
    recipe_data = {"title": lines[0].strip(), "ingredients": "", "instructions": "", "cooking_time": 0, "calories": 0, "protein": 0}

    section = ""
    for line in lines[1:]:
        line = line.strip()
        if line.lower() == "ingredients:":
            section = "ingredients"
        elif line.lower() == "instructions:":
            section = "instructions"
        elif line.lower().startswith("cooking time:"):
            recipe_data["cooking_time"] = int(line.split(":")[1].strip())
        elif line.lower().startswith("calories:"):
            recipe_data["calories"] = int(line.split(":")[1].strip())
        elif line.lower().startswith("protein:"):
            recipe_data["protein"] = int(line.split(":")[1].strip())
        elif section:
            recipe_data[section] += line + "\n"

    recipe_data["ingredients"] = recipe_data["ingredients"].strip()
    recipe_data["instructions"] = recipe_data["instructions"].strip()
    return recipe_data


@router.post("/toggle-favorite")
async def toggle_favorite(body: dict, db: AsyncSession = Depends(get_db)):
    try:
        user_id = uuid.UUID(str(body.get("user_id")))
        recipe_title = body.get("recipe_title")

        if not user_id or not recipe_title:
            raise HTTPException(status_code=422, detail="user_id and recipe_title are required")

        # First get the recipe by title
        recipe = await db.execute(select(Recipes).where(func.lower(Recipes.title) == func.lower(recipe_title)))
        recipe = recipe.scalar_one_or_none()

        # If recipe doesn't exist, create it
        if not recipe:
            recipe = Recipes(recipe_id=uuid.uuid4(), title=recipe_title, instructions="Instructions to be added", ingredients="Ingredients to be added", cooking_time=0, calories=0, protein=0)
            db.add(recipe)
            await db.commit()
            await db.refresh(recipe)

        user_prefs = await db.execute(select(UserPreferences).where(UserPreferences.user_id == user_id))
        user_prefs = user_prefs.scalar_one_or_none()

        if not user_prefs:
            user_prefs = UserPreferences(user_id=user_id, favorite_recipes=[], recipe_history=[], allergies=[], favorite_cuisines=[])
            db.add(user_prefs)

        if user_prefs.favorite_recipes is None:
            user_prefs.favorite_recipes = []

        current_favorites = list(user_prefs.favorite_recipes)

        if recipe.recipe_id in current_favorites:
            current_favorites.remove(recipe.recipe_id)
            message = f"Recipe '{recipe_title}' removed from favorites"
        else:
            current_favorites.append(recipe.recipe_id)
            message = f"Recipe '{recipe_title}' added to favorites"

        # Update the favorite_recipes with the modified list
        user_prefs.favorite_recipes = current_favorites

        await db.commit()
        return {"success": True, "message": message}
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid UUID format")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error toggling favorite recipe: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/user-preferences/{user_id}")
async def get_user_preferences(user_id: PythonUUID, db: AsyncSession = Depends(get_db)):
    try:
        user_prefs = await db.execute(select(UserPreferences).where(UserPreferences.user_id == user_id))
        user_prefs = user_prefs.scalar_one_or_none()

        if not user_prefs:
            return {"favorite_recipes": []}

        return {"favorite_recipes": user_prefs.favorite_recipes}
    except Exception as e:
        logger.error(f"Error fetching user preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/get_id")
async def get_recipe_name(recipe_title: str, db: AsyncSession = Depends(get_db)):
    print("recipe title is", recipe_title)
    query = select(Recipes.recipe_id).where(Recipes.title == recipe_title)
    result = await db.execute(query)
    recipe_id = result.scalar_one_or_none()

    if recipe_id is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"id": str(recipe_id)}  # Convert UUID to string if necessary
