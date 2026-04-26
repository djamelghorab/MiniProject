from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.model.database import get_users_collection


class UserModel:
    def __init__(self):
        self.collection = get_users_collection()

    def create_user(self, user_data):
        try:
            result = self.collection.insert_one(user_data)
            return True, str(result.inserted_id)
        except DuplicateKeyError:
            return False, "Phone number already exists."

    def get_all_users(self):
        users = list(self.collection.find())

        for user in users:
            user["_id"] = str(user["_id"])

        return users

    def search_users(self, keyword):
        query = {
            "$or": [
                {"first_name": {"$regex": keyword, "$options": "i"}},
                {"last_name": {"$regex": keyword, "$options": "i"}},
                {"birth_date": {"$regex": keyword, "$options": "i"}},
                {"birth_place": {"$regex": keyword, "$options": "i"}},
                {"phone_number": {"$regex": keyword, "$options": "i"}},
            ]
        }

        users = list(self.collection.find(query))

        for user in users:
            user["_id"] = str(user["_id"])

        return users

    def get_user_by_id(self, user_id):
        try:
            user = self.collection.find_one({"_id": ObjectId(user_id)})

            if user:
                user["_id"] = str(user["_id"])

            return user
        except Exception:
            return None

    def update_user(self, user_id, user_data):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": user_data}
            )

            if result.matched_count == 0:
                return False, "User not found."

            return True, "User updated successfully."

        except DuplicateKeyError:
            return False, "Phone number already exists."

        except Exception:
            return False, "Invalid user ID."

    def delete_user(self, user_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(user_id)})

            if result.deleted_count == 0:
                return False, "User not found."

            return True, "User deleted successfully."

        except Exception:
            return False, "Invalid user ID."
