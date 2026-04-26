import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "user_management_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "users")


def get_users_collection():
    if not MONGO_URI:
        raise ValueError("MONGO_URI is missing from .env file")

    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    client.admin.command("ping")

    db = client[DATABASE_NAME]
    users_collection = db[COLLECTION_NAME]

    users_collection.create_index(
        [("phone_number", ASCENDING)],
        unique=True
    )

    return users_collection
