import streamlit as st

# 🚫 Redirect if not authenticated
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🚫 Please log in to view your profile.")
    st.stop()

# ✅ Check if user info is present
if "user_name" not in st.session_state:
    st.warning("⚠️ User info not found. Please log in again.")
    st.stop()

# 🧾 User Profile Page
st.markdown("## 👤 User Profile")

with st.container():
    st.markdown("""
        <style>
        .profile-card {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 70%;
            margin: auto;
        }
        .profile-card h3 {
            margin-bottom: 10px;
            color: #FF5733;
        }
        .profile-card p {
            font-size: 16px;
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <h3>{st.session_state['user_name']} (ID: {st.session_state['user_id']})</h3>
    <p><strong>📧 Email:</strong> {st.session_state['user_email']}</p>
    <p><strong>📞 Phone:</strong> {st.session_state['user_phone']}</p>
    <p><strong>🎂 Age:</strong> {st.session_state['age']}</p>
    <p><strong>🌍 Country:</strong> {st.session_state['country']}</p>
    <p><strong>🏙️ Region:</strong> {st.session_state['region']}</p>
    <p><strong>🚻 Gender:</strong> {st.session_state['gender']}</p>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
