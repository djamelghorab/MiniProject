from datetime import datetime


def validate_user_data(first_name, last_name, birth_date, birth_place, phone_number):
    if not first_name.strip():
        return False, "First name is required."

    if not last_name.strip():
        return False, "Last name is required."

    if not birth_date.strip():
        return False, "Birth date is required."

    if not birth_place.strip():
        return False, "Birth place is required."

    if not phone_number.strip():
        return False, "Phone number is required."

    try:
        datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        return False, "Birth date must be in YYYY-MM-DD format."

    if not phone_number.isdigit():
        return False, "Phone number must contain only digits."

    if len(phone_number) < 10:
        return False, "Phone number must contain at least 10 digits."

    return True, "Valid user data."
