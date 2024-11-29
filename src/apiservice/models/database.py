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

import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Fetch the DATABASE_URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgresdb_preppal:5432/preppal_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    db = next(get_db())  # Use next to get the generator's first value
    print(db)
