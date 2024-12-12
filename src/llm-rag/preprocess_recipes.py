import numpy as np
import isodate
import re


# Function to convert ISO 8601 durations to a human-readable
def convert_duration_to_minutes(duration_string):
    if "-" in duration_string:
        duration_string = duration_string.replace("-", "")

    # Parse the ISO 8601 duration string
    duration = isodate.parse_duration(duration_string)

    # Get the total seconds from the duration
    total_seconds = duration.total_seconds()
    return_minutes = total_seconds / 60

    # Calculate the hours and minutes separately
    total_minutes = total_seconds // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60

    # Build the output string conditionally based on the hours and minutes
    result = []

    if hours > 0:
        hour_str = "hour" if hours == 1 else "hours"
        result.append(f"{int(hours)} {hour_str}")

    if minutes > 0:
        minute_str = "minute" if minutes == 1 else "minutes"
        result.append(f"{int(minutes)} {minute_str}")

    return " ".join(result), return_minutes


# Function to format the ingredients list
def format_ingredients(s):
    s = s.replace("c(", "").replace(")", "")
    items = re.split(r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)', s)

    return [item.strip().replace('"', "") for item in items]


# Combine quantities and ingredients into a single string
def combine_ingredients(row):
    combined = [f"{qty} {ingr}" for qty, ingr in zip(row["RecipeIngredientQuantities"], row["RecipeIngredientParts"])]
    return ", ".join(combined)


# Function to extract and format the recipe steps
def format_instructions(instructions):
    cleaned_instructions = instructions.replace("c(", "").replace(")", "")
    steps = re.findall(r'"(.*?)"', cleaned_instructions)
    cleaned_steps = [step.strip().replace("\n", "").replace('"', "") for step in steps]
    formatted_steps = [f"{i + 1}. {step}" for i, step in enumerate(cleaned_steps)]

    return "\n".join(formatted_steps)


def data_cleaning(df):
    # df = pd.read_csv("./data/recipes.csv")

    df = df.drop(
        [
            "RecipeId",
            "AuthorId",
            "AuthorName",
            "DatePublished",
            "Description",
            "Images",
            "RecipeCategory",
            "Keywords",
            "AggregatedRating",
            "ReviewCount",
            "SaturatedFatContent",
            "CholesterolContent",
            "CarbohydrateContent",
            "FiberContent",
            "RecipeYield",
        ],
        axis=1,
    )
    df = df.dropna()

    df["CookTime"], df["CookTimeMinutes"] = zip(*df["CookTime"].apply(convert_duration_to_minutes))
    df["PrepTime"], df["PrepTimeMinutes"] = zip(*df["PrepTime"].apply(convert_duration_to_minutes))
    df["TotalTime"], df["TotalTimeMinutes"] = zip(*df["TotalTime"].apply(convert_duration_to_minutes))

    df["RecipeIngredientQuantities"] = df["RecipeIngredientQuantities"].apply(format_ingredients)
    df["RecipeIngredientParts"] = df["RecipeIngredientParts"].apply(format_ingredients)

    df["Ingredients"] = df.apply(combine_ingredients, axis=1)

    df["FormattedRecipeInstructions"] = df["RecipeInstructions"].apply(format_instructions)

    df = df.drop(["RecipeInstructions", "RecipeIngredientQuantities"], axis=1)
    df.replace("", np.nan, inplace=True)
    df = df.dropna()

    return df
