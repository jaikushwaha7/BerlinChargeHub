
import streamlit as st
import src.utils.logger as lg

@lg.logger_decorator
def handle_login():
    """
    Handles the user login process.

    This function provides a way for users to input their credentials,
    validate them using the `check_credentials` function, and determine
    whether login is successful. If the login button is not pressed,
    the function assumes the user is not attempting login and returns
    a default value.

    :return: Returns the result of credential validation if the login
        process is triggered. If the login button is not pressed, it
        returns True.
    :rtype: bool
    """
    username = st.text_input("Username:", "")
    password = st.text_input("Password:", "", type="password")
    if st.button("Login to dashboard"):
        return check_credentials(username, password)


def check_credentials(username, password):
    """
    Validates user credentials based on predefined username and password.

    This function checks whether the provided username and password match the
    predefined values. It returns `True` if the credentials match and `False`
    otherwise. It also provides corresponding feedback with success or error
    messages using Streamlit.

    :param username: The username provided by the user.
    :type username: str
    :param password: The password provided by the user.
    :type password: str
    :return: A boolean value indicating whether the credentials are valid.
    :rtype: bool
    """
    if username == "admin" and password == "password":  # Example credentials
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success("Welcome to the dashboard!")
        return True
    st.error("Invalid login credentials")
    return False  # Login failed

