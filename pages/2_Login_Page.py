import streamlit as st
import settings
import supabase

settings.init()

st.set_page_config(page_title="Login", page_icon="🔒", layout="centered", initial_sidebar_state="expanded")

def login_user(email, password):
    try:
        auth_response = settings.supabase_client.auth.sign_in_with_password(credentials={"email": email, "password": password})
        if auth_response and auth_response.user:
            st.success("Logged in successfully! Go to the main page.")
            # Store user info in session state
            st.session_state.user = {
                "email": auth_response.user.email,
                "id": auth_response.user.id
            }
            return True
        else:
            st.error("Invalid email or password.")
            return False
    except Exception as e:
        st.error(f"{e}")
        return False

def main():
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if st.session_state.user:
        st.success(f"Logged in as: {st.session_state.user['email']}")
        if st.button("Logout"):
            settings.supabase_client.auth.sign_out()
            st.session_state.user = None
            st.experimental_rerun()
        return

    st.title("Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(email, password):
            st.experimental_rerun()

if __name__ == "__main__":
    main()
