import streamlit as st
import pandas as pd
from app.controller.user_controller import UserController


def show_users_table(users):
    if users:
        df = pd.DataFrame(users)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found.")


def render_user_view():
    st.set_page_config(
        page_title="User Management System",
        layout="wide"
    )

    st.title("Advanced User Management System")

    try:
        controller = UserController()
    except Exception as error:
        st.error("Database connection failed.")
        st.code(str(error))
        st.stop()

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Add User",
            "Display Users",
            "Search User",
            "Update User",
            "Delete User"
        ]
    )

    if menu == "Add User":
        st.header("Add User")

        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        birth_date = st.text_input("Birth Date", placeholder="YYYY-MM-DD")
        birth_place = st.text_input("Birth Place")
        phone_number = st.text_input("Phone Number")

        if st.button("Add User"):
            success, message = controller.add_user(
                first_name,
                last_name,
                birth_date,
                birth_place,
                phone_number
            )

            if success:
                st.success(message)
            else:
                st.error(message)

    elif menu == "Display Users":
        st.header("Display Users")

        users = controller.get_users()
        show_users_table(users)

    elif menu == "Search User":
        st.header("Search User")

        keyword = st.text_input("Search by any field")

        if keyword:
            users = controller.search_users(keyword)
            show_users_table(users)
        else:
            st.info("Enter a search keyword.")

    elif menu == "Update User":
        st.header("Update User")

        users = controller.get_users()
        show_users_table(users)

        st.subheader("Select User to Update")

        user_id = st.text_input("Enter User ID")

        if st.button("Load User"):
            user = controller.get_user_by_id(user_id)

            if user:
                st.session_state["update_user"] = user
            else:
                st.error("User not found.")

        if "update_user" in st.session_state:
            user = st.session_state["update_user"]

            first_name = st.text_input("First Name", value=user["first_name"])
            last_name = st.text_input("Last Name", value=user["last_name"])
            birth_date = st.text_input("Birth Date", value=user["birth_date"])
            birth_place = st.text_input("Birth Place", value=user["birth_place"])
            phone_number = st.text_input("Phone Number", value=user["phone_number"])

            if st.button("Update User"):
                success, message = controller.update_user(
                    user["_id"],
                    first_name,
                    last_name,
                    birth_date,
                    birth_place,
                    phone_number
                )

                if success:
                    st.success(message)
                    del st.session_state["update_user"]
                else:
                    st.error(message)

    elif menu == "Delete User":
        st.header("Delete User")

        users = controller.get_users()
        show_users_table(users)

        user_id = st.text_input("Enter User ID to delete")
        confirm_delete = st.checkbox("Are you sure ?")

        if st.button("Delete User"):
            if not confirm_delete:
                st.warning("Please confirm deletion first.")
            else:
                success, message = controller.delete_user(user_id)

                if success:
                    st.success(message)
                else:
                    st.error(message)
