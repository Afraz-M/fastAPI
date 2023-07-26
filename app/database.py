from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='afraz1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error :", error)
#         time.sleep(2)


# my_posts = [{"title": "title of post 1",
#              "content": "content of post 1", "id": 1},
#             {"title": "title of post 2",
#              "content": "content of post 2", "id": 2}]


# def find_post(id: int):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id: int):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
