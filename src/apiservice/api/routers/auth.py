from api.utils.gcs_utils import load_user_db

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.users import User
from schemas.users import UserResponse
from models.database import get_db
from api.utils.auth_utils import hash_password, validate_phone_number

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


# @router.post("/signup")
# async def signup(username: str = Form(...), password: str = Form(...)):
#     """
#     Create a new user in the GCS-stored database.
#     """
# user_db = load_user_db()

# if username in user_db:
#     raise HTTPException(status_code=400, detail="User already exists")

# # Generate a new user ID (incremental ID for simplicity)
# user_id = str(len(user_db) + 1)

# user_db[username] = {"password": password, "user_id": user_id}
# save_user_db(user_db)

# return {"message": "User created successfully", "user_id": user_id}


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(first_name: str = Form(...), last_name: str = Form(...), username: str = Form(...), phone_number: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    """
    Create a new user in the PostgreSQL database.
    """
    # Backend validation for phone number format
    if not validate_phone_number(phone_number):
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    # Hash the password
    hashed_password = hash_password(password)

    # Create a new User instance using UserCreate schema
    new_user = User(first_name=first_name, last_name=last_name, username=username, phone_number=phone_number, password=hashed_password)

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError as e:
        await db.rollback()
        # Check if the phone number or username already exists
        if "unique constraint" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="User with this phone number or username already exists")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    print("finished signup")

    return new_user
