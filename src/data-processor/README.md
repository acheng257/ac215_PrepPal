# Data Processor
<br>

This container contains the data preprocessing and training dataset generation part that is necessary for the fine-tuning of our LLM of choice (`gemini-1.5-flash-002`). This container is used as part of the ML training pipeline defined in the `src/deployment` container. It first downloads the raw dataset from our GCP bucket, preprocesses it, and turns into a train and test set. It then uploads this train and test dataset to our GCP bucket, so that the next step of the ML training pipeline can easily retrieve this data.

## General Information: Data
Our goal for the fine-tuned LLM was for it to be able to rank recipes based on ingredients available in some pantry. Thus, rather than optimizing it to be particularly verbose and great in a conversation, we wanted it to be able to take natural language (i.e. a collection of recipes) as input, and return a clearly structured and uniformly formatted output, in which the recipes are ranked based on the fit with the ingredients available. This will then allow us to use this output for further (and easier, due to the uniform format) calculation.

This presented us with several challenges:
- we needed a large collection of recipes
- we needed a reasonable pantry (just random ingredients would not have been particularly useful, as we wanted to fine-tune the LLM to pick the best recipes based on ingredient fit. If a pantry only contains very specific ingredients, there often will be no or only very little fit.)
- we needed a ranking algorithm given some recipes so that we could fine-tune the LLM for our specific task

### Collection of Recipes
For the large collection of recipes, we used the [All-Recipes Dataset](https://huggingface.co/datasets/corbt/all-recipes) available through HuggingFace. This dataset contains 2,231,142 recipes with their respective titles, their ingredients (and their quantities), and their cooking directions. After cleaning (dropping all recipes that contain weird characters, as well as all recipes that contain ingredients that occur less than 501 times), we were left with 1,297,716 recipes. Both the original dataset (full_dataset.csv) and the cleaned version (reduced_dataset.csv) have been stored in a private GCP (Google Cloud Platform) data bucket. All of this has been performed in the notebook explore_finetuning_data.ipynb.

### Reasonable Pantry
Given the cleaned dataset, we computed an ingredient-frequency dictionary and used a weighted-sampling algorithm (using the frequencies as weights) to sample 35 non-reccuring ingredients. This is the random pantry we used in each fine-tuning datapoint (each fine-tuning datapoint had a different random pantry).

### Ranking Algorithm
We had two goals for ranking a collection of recipes. First, we wanted to make sure that recipes are prioritized for which the user already has most of the ingredients in their pantry. Secondly, we wanted to make sure that recipes are prioritized for which the user would have to buy as little new ingredients as possible. We used a balanced approach and tried to balance these two different metrics evenly. For the exact implementation, please see the **`sort_recipes()`** method in **`src/data-processor/hepler.py`**.


## Basic Rundown (TL;DR)
If you want to generate and upload new data without immediately training a model afterwards, you can follow the following steps:
- Make sure you are inside the `src/data-processor` folder and open a terminal at this location
- Run `sh docker-shell.sh`

Once in the container, generate, and prepare and upload the dataset to the GCP bucket
- Run `python cli.py --generate` to generate a new question-answer LLM fine-tune dataset
- Run `python cli.py --prepare` to split data into train and test and upload them to GCP


## Generate Question Answer Dataset
*Note: this section is to large parts copied from https://github.com/dlops-io/llm-finetuning/blob/main/README.md*

### Number of Iterations for Question Generation

The user can specify the size of the training data by specifiying the number of iterations in the creation of the dataset. By using the argument `python cli.py --generate --data-iterations 100`, `data-processor` will create a dataset with 100 (pantry, 5 recipes --> 5 ranked recipes) combinations. Change the number of iterations to build a larger/smaller dataset. It will cost approximately $1.0 for 34 iterations (if trained for 3 epochs).

*Note: we trained our model for 5100 iterations for 3 epochs (using $150).*


### Sample Question Answers

As previously mentioned, every training data point includes the ingredients available in a pantry and 5 recipes, followed by the question: `Based on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible.`. Every answer will be the ranking of the recipes, followed by which ingredients the user is missing for that specific recipe.

Here is one sample result from when you run the `--generate` option from the above step:

```
[
  {
    "question": "Here are the ingredients you have available in your pantry: salt, sugar, water, olive oil, pepper, cornmeal, lime juice, white wine vinegar, flour, fresh mint, garlic, apples, portobello mushrooms, eggs, tomatoes, vanilla pudding, cream cheese, green tomatoes, potatoes, oats, vanilla, nuts, bean sprouts, popcorn, chili powder, mozzarella cheese, tabasco sauce, baking soda, onion, mustard, bread crumbs, light brown sugar, frozen, red pepper, onions. Here are the suggested recipes: - TITLE OF RECIPE: Beet and Parsley Salad. INGREDIENTS AND THEIR QUANTITIES: 2 medium beets without greens, 1 cup packed fresh flat-leaf parsley leaves, 1/4 teaspoon salt, or to taste, 1/4 teaspoon sugar, or to taste, 1/8 teaspoon black pepper, 2 teaspoons extra-virgin olive oil, 2 teaspoons balsamic vinegar, Special equipment: a Japanese Benriner* or other adjustable-blade slicer. DIRECTIONS: Step 1. Trim and peel raw beets, then cut into very thin slices (1/16 inch thick) with slicer. Step 2. Make small stacks of slices and cut each stack with a sharp knife into very thin strips (1/16 inch thick). Step 3. Toss beets with parsley, salt, sugar, and pepper in a serving bowl until sugar is dissolved. Step 4. Add oil and toss to coat. Step 5. Sprinkle vinegar on salad and toss again. Step 6. Serve immediately. Step 7. *Available at Asian markets, some cookware shops, and Uwajimaya (800-889-8801). END OF RECIPE.    - TITLE OF RECIPE: Spicy Lamb With Zucchini And Spicy Yogurt Sauce. INGREDIENTS AND THEIR QUANTITIES: Spicy Lamb with Zucchini, 4 -5 zucchini, cut length-wise and sliced, 1 lb ground lamb, 2 garlic cloves, finely chopped, 1 vidalia onion, minced, 2 teaspoons cayenne pepper, 1 teaspoon fresh ground black pepper, 1 teaspoon kosher salt, 1 tablespoon extra virgin olive oil, Spicy Yogurt Sauce, 1 cup plain yogurt, 1 green onion, finely chopped, 2 tablespoons fresh cilantro, finely chopped, 1 teaspoon cumin, 1/4 cup cucumber, finely chopped, 1 teaspoon fresh ground black pepper, 1 garlic clove, finely chopped (optional). DIRECTIONS: Step 1. Make the sauce a day ahead, or at the least, a few hours ahead to allow the flavors to properly meld together. Step 2. Add all the ingredients for the sauce into a food processor and mix until well blended. If you don't have a food processor, just chop as finely as you can. Place in a sealed container in your refrigerator. Step 3. In a large saucepan over medium heat, saute the zucchini and garlic in the olive oil. Step 4. In a cast iron pan, cook the lamb with the onions until the lamb is brown and the onions are soft. Step 5. Add the zucchini and garlic to the lamb, mix well. Step 6. Serve with the Spicy Yogurt Sauce over top. You can also serve it on rice, if you like. END OF RECIPE.    - TITLE OF RECIPE: Freezer Breakfast Burritos. INGREDIENTS AND THEIR QUANTITIES: 1/2 cup chopped onions, 1 cup diced mushrooms, 2 cups chopped spinach, 2 cups eggs ( I used 4 eggs and 1 cup egg whites, but any combo will work), taco seasonings packet, 1 cup diced tomatoes, 12-16 oz cooked ground turkey/sausage, 12 tortillas (low-card, sprouted grain and whole wheat are all great light options), low fat cheese, optional. DIRECTIONS: Step 1. Saute onions in a little cooking spray until translucent and tender, just a few minutes. Add mushrooms and spinach. Allow spinach to wilt. Step 2. Whisk eggs and egg whites together. Pour into heated skillet and scramble eggs until cooked. Step 3. Add meat, taco seasoning, and tomatoes, stirring well to combine and coat. Step 4. Fill tortillas with mixture and top with a pinch of low fat cheese if desired Step 5. Fold tortillas into burritos, tucking in the sides so the filling is fully enclosed, and wrap in plastic\nwrap to maintain form. Freeze! Step 6. When you're ready to enjoy, reheat in microwave for\nabout 1-2 minutes, turning halfway END OF RECIPE.    - TITLE OF RECIPE: Tea Cakes. INGREDIENTS AND THEIR QUANTITIES: 4 eggs, 2 c. sugar, 1/2 c. milk, 3 c. flour, 1/2 lb. butter, 1 tsp. vanilla. DIRECTIONS: Step 1. Put eggs in medium sized bowl; beat them well. Step 2. Add sugar, milk, butter and vanilla. Step 3. Now add flour and mix well to make a soft dough. Step 4. Drop from tablespoon on cookie sheet and bake at 350\u00b0 for about 10 minutes or until golden brown. END OF RECIPE.    - TITLE OF RECIPE: Broccoli Casserole. INGREDIENTS AND THEIR QUANTITIES: 2 pkg. frozen broccoli, 1 bunch green onion, 1 can water chestnuts, 1 pkg. shredded cheese, 1 small sour cream, 1 can mushroom soup, bread crumbs. DIRECTIONS: Step 1. Grease casserole dish. Step 2. Run hot water over broccoli and place in dish. Step 3. Dice green onion and sprinkle over broccoli. Step 4. Drain chestnuts. Step 5. Pour over top. Step 6. Mix cheese, soup and sour cream together. Step 7. Pour over top of broccoli. Step 8. Pour bread crumbs over top. Cook 1 hour at 325\u00b0. END OF RECIPE.    . Based on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible.",
    "answer": "Rank 1: Tea Cakes. Rank 1 has been chosen for this recipe because you have 4 out of 6 ingredients in your pantry! Here are the ingredients you still need: milk, butter. Rank 2: Beet and Parsley Salad. Rank 2 has been chosen for this recipe because you have 2 out of 6 ingredients in your pantry! Here are the ingredients you still need: parsley, black pepper, extra-virgin olive oil, balsamic vinegar. Rank 3: Freezer Breakfast Burritos. Rank 3 has been chosen for this recipe because you have 3 out of 9 ingredients in your pantry! Here are the ingredients you still need: mushrooms, chopped spinach, taco, sausage, tortillas, cheese. Rank 4: Broccoli Casserole. Rank 4 has been chosen for this recipe because you have 1 out of 7 ingredients in your pantry! Here are the ingredients you still need: frozen broccoli, green onion, water chestnuts, shredded cheese, sour cream, mushroom soup. Rank 5: Spicy Lamb With Zucchini And Spicy Yogurt Sauce. Rank 5 has been chosen for this recipe because you have 1 out of 16 ingredients in your pantry! Here are the ingredients you still need: zucchini, zucchini, ground lamb, vidalia onion, cayenne pepper, fresh ground black pepper, kosher salt, extra virgin olive oil, plain yogurt, green onion, fresh cilantro, cumin, cucumber, fresh ground black pepper. "
  }
  ...
]
```

These data points are then converted into a csv format.


### Upload Dataset
- Run `python cli.py --prepare`
- This step will take the generated `.csv` file, split it into a train (85%) and test (15%) set and upload them to GCP as csv and jsonl files.

For Gemini fine-tuning the required data format is as shown below:
```
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {
          "text": question
        }
      ]
    },
    {
      "role": "model",
      "parts": [
        {
          "text": answer
        }
      ]
    }
  ]
}
```
