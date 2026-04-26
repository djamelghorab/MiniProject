from app.model.user_model import UserModel
from app.model.validation import validate_user_data


class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def add_user(self, first_name, last_name, birth_date, birth_place, phone_number):
        is_valid, message = validate_user_data(
            first_name,
            last_name,
            birth_date,
            birth_place,
            phone_number
        )

        if not is_valid:
            return False, message

        user_data = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "birth_date": birth_date.strip(),
            "birth_place": birth_place.strip(),
            "phone_number": phone_number.strip()
        }

        success, result = self.user_model.create_user(user_data)

        if success:
            return True, "User added successfully."

        return False, result

    def get_users(self):
        return self.user_model.get_all_users()

    def search_users(self, keyword):
        if not keyword.strip():
            return []

        return self.user_model.search_users(keyword.strip())

    def get_user_by_id(self, user_id):
        return self.user_model.get_user_by_id(user_id)

    def update_user(self, user_id, first_name, last_name, birth_date, birth_place, phone_number):
        is_valid, message = validate_user_data(
            first_name,
            last_name,
            birth_date,
            birth_place,
            phone_number
        )

        if not is_valid:
            return False, message

        user_data = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "birth_date": birth_date.strip(),
            "birth_place": birth_place.strip(),
            "phone_number": phone_number.strip()
        }

        return self.user_model.update_user(user_id, user_data)

    def delete_user(self, user_id):
        return self.user_model.delete_user(user_id)
