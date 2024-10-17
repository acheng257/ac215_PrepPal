import os
import argparse
import pandas as pd
import json
import time
import glob
from google.cloud import storage
import vertexai
from vertexai.preview.tuning import sft
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
TRAIN_DATASET = "gs://preppal-data/llm-finetune-dataset-small/train.jsonl" # Replace with your dataset
VALIDATION_DATASET = "gs://preppal-data/llm-finetune-dataset-small/test.jsonl" # Replace with your dataset
GCP_LOCATION = "us-central1"
GENERATIVE_SOURCE_MODEL = "gemini-1.5-flash-002" # gemini-1.5-pro-002

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)

def train(wait_for_job=False):
    print("train()")

    # Supervised Fine Tuning
    sft_tuning_job = sft.train(
        source_model=GENERATIVE_SOURCE_MODEL,
        train_dataset=TRAIN_DATASET,
        validation_dataset=VALIDATION_DATASET,
        epochs=3, # change to 2-3
        adapter_size=4,
        learning_rate_multiplier=1.0,
        tuned_model_display_name="preppal-small-v1",
    )
    print("Training job started. Monitoring progress...\n\n")
    
    # Wait and refresh
    time.sleep(60)
    sft_tuning_job.refresh()
    
    if wait_for_job:
        print("Check status of tuning job:")
        print(sft_tuning_job)
        while not sft_tuning_job.has_ended:
            time.sleep(60)
            sft_tuning_job.refresh()
            print("Job in progress...")

    print(f"Tuned model name: {sft_tuning_job.tuned_model_name}")
    print(f"Tuned model endpoint name: {sft_tuning_job.tuned_model_endpoint_name}")
    print(f"Experiment: {sft_tuning_job.experiment}")


def chat():
    print("chat()")
    # Get the model endpoint from Vertex AI: https://console.cloud.google.com/vertex-ai/studio/tuning?project=ac215-project
    MODEL_ENDPOINT = "projects/582280928569/locations/us-central1/endpoints/3898306381651902464" # Finetuned model
    
    generative_model = GenerativeModel(MODEL_ENDPOINT)

    query = "Here are the ingredients you have available in your pantry: salt, sugar, water, olive oil, pepper, extra lean ground beef, noodles, flour, fruit cocktail, ground coriander, rice, boiling water, onion soup, vanilla, warm water, peaches, tomatoes, onion, ground ginger, cottage cheese, mushroom stems, pineapple, lime, butter, lemon juice, white vinegar, cheese, taco sauce, yellow cake mix, powdered sugar, baking powder, pinto beans, sour cream, bread crumbs, pimiento. Here are the suggested recipes: - TITLE OF RECIPE: Grown-Up Carrot Cake. INGREDIENTS AND THEIR QUANTITIES: 300 g plain flour, 3 teaspoons cinnamon, 2 teaspoons ground ginger, 1/2 teaspoon bicarbonate of soda, 1 teaspoon baking powder, 200 g brown sugar, 4 eggs, 250 ml sunflower oil, 1 orange, zest of, 1 lemon, zest of, 200 g carrots, finely grated, 150 g chopped walnuts, 125 g unsalted butter, 50 g icing sugar, 250 g cream cheese. DIRECTIONS: Step 1. Heat your oven to 150\u00b0C. Step 2. Sift the flour, cinnamon, ginger, baking powder and bicarbonate of soda into a bowl and mix together with the sugar. Step 3. In another bowl, beat the eggs, oil and zests together, then add the carrots and walnuts. Step 4. Fold into the flour mixture. Step 5. Pour into a greased and lined tin and bake for 1 hour 20 minutes, or until a skewer comes out cleanly. Once cooked, turn out and let cool. Step 6. Meanwhile, beat together the icing sugar and butter until light and fluffy, then fold in the cream cheese. Put in the fridge until stiffened. Step 7. Once the cake is cool, spread the topping over and serve. END OF RECIPE.    - TITLE OF RECIPE: Flank Steak Teriyaki. INGREDIENTS AND THEIR QUANTITIES: 1/4 c. soy sauce, 2 Tbsp. onion flakes, 2 Tbsp. vinegar, 1/2 tsp. powdered ginger, 2 tsp. Sweet 'N Low or sugar, 1/4 tsp. garlic (powdered or oil). DIRECTIONS: Step 1. Mix all ingredients together well. Step 2. Take a 1 to 1 1/2 pound piece of flank steak (or round steak or Swiss steak) and make several lengthwise cuts partially through the steak. Step 3. Place steak in baking dish and pour marinade over the meat. Step 4. Turn several times to spread the marinade. Step 5. Cover pan and place in refrigerator, turning meat several times to soak up marinade. (Best if left to marinade overnight.) Step 6. Broil or grill to desired doneness. END OF RECIPE.    - TITLE OF RECIPE: Artichoke Dip. INGREDIENTS AND THEIR QUANTITIES: 1 can artichokes, 1 c. mayonnaise, 1 c. Parmesan cheese. DIRECTIONS: Step 1. Mash artichokes. Step 2. Mix mayonnaise and Parmesan cheese. Step 3. Bake 30 minutes at 350\u00b0. Step 4. Serve with wheat crackers. END OF RECIPE.    - TITLE OF RECIPE: Chicken Casserole. INGREDIENTS AND THEIR QUANTITIES: 1 c. diced chicken, 1 c. diced celery, 1 can cream of chicken soup, 1/2 c. slivered almonds, 1 tsp. to 2 Tbsp. onion, grated, 1 Tbsp. lemon juice, 1/4 tsp. pepper, 1/2 tsp. salt, 3 diced hard-cooked eggs, 1/2 c. mayonnaise, 2 c. potato chips. DIRECTIONS: Step 1. This was served at my mother's 80th birthday party. END OF RECIPE.    - TITLE OF RECIPE: Orange Congealed Salad. INGREDIENTS AND THEIR QUANTITIES: 2 (3 oz.) pkg. orange jello, 1/2 c. mayonnaise, 1 large can crushed pineapple (with juice), 1 large can evaporated milk, 1 c. chopped nuts. DIRECTIONS: Step 1. Dissolve jello in 2 cups boiling water and set aside to cool. Whip the mayonnaise with a mixer until fluffy. Stir in milk, pineapple and nuts. Step 2. Pour into a mold and refrigerate until ready to serve. END OF RECIPE.    . Based on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible.?"
    print("query: ",query)
    response = generative_model.generate_content(
        [query],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
    )
    generated_text = response.text
    print("Fine-tuned LLM Response:", generated_text)
     

def main(args=None):
    print("CLI Arguments:", args)

    if args.train:
        train()
    
    if args.chat:
        chat()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--train",
        action="store_true",
        help="Train model",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Chat with model",
    )

    args = parser.parse_args()

    main(args)