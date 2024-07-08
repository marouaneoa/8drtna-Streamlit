import streamlit as st
import settings
from streamlit_extras.switch_page_button import switch_page

settings.init()

def register_user(email, password):
    try:
        credentials = {
            "email": email,
            "password": password
        }
        user = settings.supabase_client.auth.sign_up(credentials)
        if user:
            st.success("Registered successfully! Please log in.")
            return True
        else:
            st.error("Registration failed.")
            return False
    except Exception as e:
        st.error(f"{e}")
        return False

def main():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.success("You are already logged in!")
        if st.button("Go to Main Page"):
            switch_page("Main")  
        return

    st.title("Sign Up Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if register_user(email, password):
            if st.button("Go to Login"):
                switch_page("Login")  

if __name__ == "__main__":
    main()
