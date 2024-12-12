# import sqlalchemy.orm
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/preppal_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/preppal_db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = sqlalchemy.orm.declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# if __name__ == "__main__":
#     db = get_db()
#     print(db)

# database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Fetch the DATABASE_URL from environment variables or use a default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@postgresdb_preppal:5432/preppal_db")

# Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async sessionmaker
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Define the declarative base
Base = declarative_base()


# Dependency to get the async session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Optional: Function to initialize the database (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# import sqlalchemy.orm
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# # Fetch the DATABASE_URL from environment variables
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgresdb_preppal:5432/preppal_db")

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = sqlalchemy.orm.declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# if __name__ == "__main__":
#     db = next(get_db())  # Use next to get the generator's first value
#     print(db)
