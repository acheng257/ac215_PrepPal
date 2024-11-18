from fastapi import APIRouter, Form, HTTPException
from api.utils.gcs_utils import load_user_db, save_user_db

router = APIRouter()


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Authenticate user against the GCS-stored database.
    """
    user_db = load_user_db()
    user = user_db.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"user_id": user["user_id"]}


@router.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...)):
    """
    Create a new user in the GCS-stored database.
    """
    user_db = load_user_db()

    if username in user_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Generate a new user ID (incremental ID for simplicity)
    user_id = str(len(user_db) + 1)

    user_db[username] = {"password": password, "user_id": user_id}
    save_user_db(user_db)

    return {"message": "User created successfully", "user_id": user_id}
