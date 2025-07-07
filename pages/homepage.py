import streamlit as st

# 🔐 Redirect if not logged in
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("You must log in first to view this page.")
    st.stop()

# ---------- Global CSS ----------
st.markdown("""
    <style>
    .title-style {
        font-size: 48px;
        font-weight: 700;
        color: #FF5733;
        margin-top: -20px;
        margin-bottom: 10px;
    }

    .description-style {
        font-size: 18px;
        color: #333;
        margin-bottom: 20px;
    }

    .section-container {
        background-color: #f9f9f9;
        padding: 25px;
        margin-bottom: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f1f1f1;
        padding: 20px;
        border-radius: 15px;
        width: fit-content;
        margin: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .button-style {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }

    .top-bar {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 10px 20px;
        background-color: #ffffff;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        margin-bottom: 15px;
    }

    .user-buttons {
        display: flex;
        gap: 10px;
    }

    </style>
""", unsafe_allow_html=True)

# ---------- Top Navigation Bar ----------
with st.container():
    st.markdown('<div class="top-bar">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([6, 2, 1])

    with col2:
        if st.button(f"👤 {st.session_state.get('user_name', 'User')}"):
            st.switch_page("pages/user_profile.py")

    with col3:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Logged out successfully!")
            st.switch_page("app.py")  # Change to your login page if needed

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Header Section ----------
with st.container():
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title-style">🛍️ Shopify</h1>', unsafe_allow_html=True)
    st.markdown('<p class="description-style">Welcome! This will be your interface to search through e-commerce products using Elasticsearch 🔍</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Search Bar Section ----------
with st.container():
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search for products", placeholder="Enter product name or keywords")
    if search_query:
        st.session_state["keyword"] = search_query.strip()
        st.switch_page("pages/searchpage.py")


# ---------- Electronics Section ----------
with st.container():
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("## 💻 Shop Electronics")
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("Image/electronics1.jpg", width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-style">', unsafe_allow_html=True)
    if st.button("🛒 Shop Now - Electronics"):
        st.session_state["selected_category"] = "Electronics"  # 🔁 Pass tag
        st.switch_page("pages/Category_search.py")
 # 🔁 Redirect
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Home Decor Section ----------
with st.container():
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("## 🪑 Shop Home stuffs")
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("Image/home_decor1.jpg", width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-style">', unsafe_allow_html=True)
    if st.button("🛒 Shop Now - Home"):
        st.session_state["selected_category"] = "Home"  # 🔁 Pass tag
        st.switch_page("pages/Category_search.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Water Bottles Section ----------
with st.container():
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("## 💧 Shop Water Bottles")
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("Image/water_bottle.webp", width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-style">', unsafe_allow_html=True)
    if st.button("🛒 Shop Now - Bottles"):
        st.session_state["selected_category"] = "Bottles"  # 🔁 Pass tag
        st.switch_page("pages/Category_search.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Offers Section ----------
with st.container():
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown("## 🔥 Shop Deals & Offers")
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("Image/offers.jpg", width=300)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="button-style">', unsafe_allow_html=True)
    if st.button("🛒 Shop Now - Offer products"):
        # 🔁 Pass tag
        st.switch_page("pages/offer_page.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
