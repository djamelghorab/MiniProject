from datetime import datetime

import pandas as pd
import streamlit as st

from app.controller.user_controller import UserController


def show_users_table(users):
    if users:
        df = pd.DataFrame(users)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found.")


def show_users_with_actions(users, controller):
    if not users:
        st.info("No users found.")
        return

    header = st.columns([2, 2, 2, 2, 2, 1, 1])
    header[0].markdown("**First Name**")
    header[1].markdown("**Last Name**")
    header[2].markdown("**Birth Date**")
    header[3].markdown("**Birth Place**")
    header[4].markdown("**Phone Number**")
    header[5].markdown("**Edit**")
    header[6].markdown("**Delete**")

    st.divider()

    for user in users:
        user_id = str(user.get("_id", ""))

        col1, col2, col3, col4, col5, col6, col7 = st.columns(
            [2, 2, 2, 2, 2, 1, 1]
        )

        col1.write(user.get("first_name", ""))
        col2.write(user.get("last_name", ""))
        col3.write(user.get("birth_date", ""))
        col4.write(user.get("birth_place", ""))
        col5.write(user.get("phone_number", ""))

        if col6.button("✏️", key=f"edit_{user_id}", help="Edit user"):
            st.session_state["update_user"] = user
            st.session_state["menu"] = "Update User"
            st.rerun()

        if col7.button("🗑️", key=f"delete_{user_id}", help="Delete user"):
            st.session_state["delete_user"] = user
            st.session_state["menu"] = "Delete User"
            st.rerun()


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

    menu_items = [
        "Add User",
        "Display Users",
        "Search User",
        "Update User",
        "Delete User"
    ]

    if "menu" not in st.session_state:
        st.session_state["menu"] = "Add User"

    menu = st.sidebar.radio(
        "Navigation",
        menu_items,
        index=menu_items.index(st.session_state["menu"])
    )

    st.session_state["menu"] = menu

    if menu == "Add User":
        st.header("Add User")

        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")

        birth_date = st.date_input("Birth Date")
        birth_date = birth_date.strftime("%Y-%m-%d")

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
        show_users_with_actions(users, controller)

    elif menu == "Search User":
        st.header("Search User")

        keyword = st.text_input("Search by any field")

        if keyword:
            users = controller.search_users(keyword)
            show_users_with_actions(users, controller)
        else:
            st.info("Enter a search keyword.")

    elif menu == "Update User":
        st.header("Update User")

        users = controller.get_users()

        st.subheader("Select a user from the list")
        show_users_with_actions(users, controller)

        if "update_user" in st.session_state:
            user = st.session_state["update_user"]

            st.divider()
            st.subheader("Edit Selected User")

            first_name = st.text_input(
                "First Name",
                value=user.get("first_name", ""),
                key="update_first_name"
            )

            last_name = st.text_input(
                "Last Name",
                value=user.get("last_name", ""),
                key="update_last_name"
            )

            try:
                birth_date_value = datetime.strptime(
                    user.get("birth_date", ""),
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                birth_date_value = datetime.today().date()

            birth_date = st.date_input(
                "Birth Date",
                value=birth_date_value,
                key="update_birth_date"
            )
            birth_date = birth_date.strftime("%Y-%m-%d")

            birth_place = st.text_input(
                "Birth Place",
                value=user.get("birth_place", ""),
                key="update_birth_place"
            )

            phone_number = st.text_input(
                "Phone Number",
                value=user.get("phone_number", ""),
                key="update_phone_number"
            )

            if st.button("Save Changes"):
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
                    st.rerun()
                else:
                    st.error(message)

    elif menu == "Delete User":
        st.header("Delete User")

        users = controller.get_users()

        st.subheader("Select a user from the list")
        show_users_with_actions(users, controller)

        if "delete_user" in st.session_state:
            user = st.session_state["delete_user"]

            st.divider()
            st.warning(
                f"Are you sure you want to delete "
                f"{user.get('first_name', '')} {user.get('last_name', '')}?"
            )

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this user"
            )

            col1, col2 = st.columns([1, 1])

            if col1.button("Confirm Delete"):
                if not confirm_delete:
                    st.warning("Please confirm deletion first.")
                else:
                    success, message = controller.delete_user(user["_id"])

                    if success:
                        st.success(message)
                        del st.session_state["delete_user"]
                        st.rerun()
                    else:
                        st.error(message)

            if col2.button("Cancel"):
                del st.session_state["delete_user"]
                st.rerun()
