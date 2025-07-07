import streamlit as st
from utils.auth import authenticate_user, user_info

# Initialize session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Login page
def login_page():
    st.markdown("## 🔐 Login to Shopify")
    user_id = st.text_input("👤 User ID")
    password = st.text_input("🔑 Password", type="password")

    if st.button("🔓 Login"):
        if password.isdigit() and authenticate_user(user_id, password):
            st.session_state["authenticated"] = True
            st.success("Login successful ✅")
            user_info(user_id)
            st.switch_page("pages/homepage.py")
        else:
            st.error("❌ Invalid user ID or password")

# Check session
if not st.session_state["authenticated"]:
    login_page()
else:
    st.switch_page("pages/homepage.py")
