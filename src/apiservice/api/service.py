from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import pantry, auth, llm_chat, recipes, user_history

# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to Preppal"}


# Additional routers here
app.include_router(recipes.router, prefix="/recipes")
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(pantry.router, prefix="/pantry")
app.include_router(llm_chat.router, prefix="/llm")
app.include_router(user_history.router, prefix="")
