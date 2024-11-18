from fastapi import FastAPI, Form, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict

app = FastAPI(title="AI-Powered Chat and Recommendation API", version="v2")

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_history = []
file_content = None
users = {"test@test.com": "aaa"}
pantry = {}

# for testing
recipes = [
    {
        "name": "Pasta Primavera",
        "cookingTime": "25 mins",
        "ingredients": ["pasta", "vegetables", "olive oil"],
        "calories": 320,
    },
    {
        "name": "Grilled Salmon",
        "cookingTime": "20 mins",
        "ingredients": ["salmon", "lemon", "herbs"],
        "calories": 420,
    },
    {
        "name": "Chicken Stir-Fry",
        "cookingTime": "15 mins",
        "ingredients": ["chicken", "vegetables", "soy sauce"],
        "calories": 500,
    },
    {
        "name": "Quinoa Bowl",
        "cookingTime": "30 mins",
        "ingredients": ["quinoa", "avocado", "chickpeas"],
        "calories": 400,
    },
]

# Replace with our own model
# recommendation_model = pipeline("text-generation")


# User login endpoints
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[username] = password
    return {"message": f"User {username} registered successfully"}


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if users.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": f"User {username} logged in successfully"}


@app.post("/logout")
async def logout(username: str = Form(...)):
    # Simulated logout logic
    return {"message": f"User {username} logged out successfully"}


# Pantry update endpoint
@app.post("/update_pantry")
async def update_pantry(
    add: Optional[Dict[str, int]] = Body(None),
    subtract: Optional[Dict[str, int]] = Body(None),
):
    global pantry

    if add:
        for ingredient, quantity in add.items():
            pantry[ingredient] = pantry.get(ingredient, 0) + quantity

    if subtract:
        for ingredient, quantity in subtract.items():
            if pantry.get(ingredient, 0) < quantity:
                raise HTTPException(status_code=400, detail=f"Not enough {ingredient} in pantry")
            pantry[ingredient] -= quantity

    return {"message": "Pantry updated", "pantry": pantry}


# Recommendation generation endpoint
@app.post("/get_recs")
async def get_recs(filters: dict = Body(...), more_recommendations: bool = False):
    # recommendation_model = None
    # prompt = f"Based on the following filters: {filters}, suggest some recipes."
    # recommendations = recommendation_model(prompt, max_length=50, num_return_sequences=5)
    # recipes = [rec['generated_text'] for rec in recommendations]

    # if more_recommendations:
    #     more_recs = recommendation_model(prompt + " Provide more options.", max_length=50, num_return_sequences=5)
    #     recipes.extend([rec['generated_text'] for rec in more_recs])

    # return {"recommendations": recipes}
    print("Success")
    return {"recommendations": recipes}


# General chatbot endpoint
# @app.post("/chat_gemini")
# async def chat(message: str = Form(...)):
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     if not GEMINI_API_KEY:
#         raise ValueError("GEMINI_API_KEY environment variable is not set.")
#     genai.configure(api_key=GEMINI_API_KEY)
#     gemini_model = genai.GenerativeModel("gemini-1.5-flash")

#     global chat_history
#     chat_history.append({"user": message})
#     response = gemini_model.generate_text(prompt=message).text
#     chat_history.append({"bot": response})
#     return {"response": response, "chat_history": chat_history}


# Basic route for index
@app.get("/")
async def get_index():
    return {"message": "Welcome to Preppal"}


@app.post("/test")
async def test():
    print("test successful")
    return {"message": "Test successful"}
