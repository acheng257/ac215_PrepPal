from fastapi import FastAPI, Form, HTTPException, APIRouter
from firebase_admin import credentials, auth, initialize_app
import os

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.environ['FIREBASE_AUTH'])
initialize_app(cred)

router = APIRouter()

# Login Route
@router.post("/")
async def login(username: str = Form(...), password: str = Form(...)):
    print("hi")
    try:
        # Simulate login by generating a custom token
        user = auth.get_user_by_email(username)
        custom_token = auth.create_custom_token(user.uid)
        return {"token": custom_token.decode("utf-8")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.get("/hi")
async def login():
    return {"hi":"hi"}

# Sign-Up Route
@router.post("/signup")
async def signup(email: str = Form(...), password: str = Form(...), display_name: str = Form(None)):
    try:
        # Create a new user
        user = auth.create_user(email=email, password=password, display_name=display_name)
        return {"message": "User created successfully", "user_id": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Password Reset Route
@router.post("/reset-password")
async def reset_password(email: str = Form(...)):
    try:
        # Send password reset email
        link = auth.generate_password_reset_link(email)
        return {"message": "Password reset email sent", "link": link}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

