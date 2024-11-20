from fastapi import APIRouter
from api.utils.llm_rag_utils import generate_recommendation_list

router = APIRouter()


@router.post("/get_recs")
async def get_recs(body: dict):
    cooking_time = body["cookingTime"]
    serving_size = body["servings"]
    cuisine = body["cuisine"]
    ingredients_query = ", ".join(body["ingredients"])
    print("Cooking Time:", cooking_time, "Serving Size:", serving_size, "Cuisine:", cuisine)

    content_dict = {"ingredients": ingredients_query, "pantry": "sugar, pepper, broccoli, penne pasta, tomatoes, potatoes, flour"}
    recommendations = generate_recommendation_list(content_dict)

    rankings = recommendations["ranking"]
    list_of_recipes = recommendations["possible_recipes"]

    recipes_dicts = []
    for recipe in list_of_recipes.split("Recipe: ")[1:]:
        title, recipe = recipe.split("\nRecipe Servings: ")
        servings, recipe = recipe.split("\nTotal Time: ")
        time, recipe = recipe.split("\nIngredients: ")
        ingredients, recipe = recipe.split("\nCalories: ")
        calories, recipe = recipe.split("\nSugar")
        _, instructions = recipe.split("\nInstructions: ")
        instructions = instructions.split("\n")[:-1]

        recipe_dict = {"title": title, "time": time, "servings": servings, "ingredients": ingredients.split(", "), "calories": calories, "instructions": instructions}
        recipes_dicts.append(recipe_dict)

    print(rankings)

    rankings = rankings.split("Rank 1: ")[-1]
    rank1, rankings = rankings.split("Rank 2: ")
    rank2, rankings = rankings.split("Rank 3: ")
    rank3, rankings = rankings.split("Rank 4: ")
    rank4, rank5 = rankings.split("Rank 5: ")

    all_rankings = [rank1, rank2, rank3, rank4, rank5]
    all_rankings = [ranking.split("\n") for ranking in all_rankings]
    all_rankings[-1] = all_rankings[-1][:-2]

    ordered_recipe_dicts = []
    while all_rankings:
        current_ranking_title, missing_ingredients = all_rankings[0]

        for recipe_dict in recipes_dicts:
            if recipe_dict["title"] == current_ranking_title:
                recipe_dict["missing_ingredients"] = missing_ingredients.split("Here are the ingredients you still need: ")[-1][:-2].split(", ")
                ordered_recipe_dicts.append(recipe_dict)

        all_rankings = all_rankings[1:]

    # import json
    # with open("recipe_recommendations.json", 'w') as json_file:
    #     json.dump(ordered_recipe_dicts, json_file, indent=4)

    return {"recommendations": ordered_recipe_dicts}
