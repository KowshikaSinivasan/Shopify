import streamlit as st
from utils.search import search_and_get_products

# ---------- CONFIG ----------
st.set_page_config(page_title="Search", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        transition: 0.3s ease-in-out;
        background-color: #ffffff;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .product-card:hover {
        box-shadow: 0 8px 24px rgba(15,15,15,0.15);
        transform: translateY(-6px);
    }
    .product-image {
        border-radius: 8px;
        width: 100%;
        transition: 0.3s ease-in-out;
    }
    .product-image:hover {
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Get Keyword from Session ----------
query = st.session_state.get("keyword", "").strip()

if not query:
    st.warning("⚠️ No search keyword provided.")
    st.stop()

st.title(f"🔎 Results for: {query}")

# ---------- Sort Option ----------
sort_option = st.selectbox(
    "🔃 Sort By",
    ["Best Match (Weighted)", "Price: Low to High", "Price: High to Low", "Rating: High to Low"]
)

# ---------- WEIGHTS for RANKING ----------
WEIGHTS = {
    "discount": 0.7,
    "rating": 0.3,
    "boost": 0.5  # for sponsored
}

def compute_score(product):
    if product["inventory"] == 0:
        return -1000  # bury out of stock
    discount = product["price"].get("discount", 0)
    rating = product["sales"].get("avg_rating", 0)
    base_score = (discount / 100.0) * WEIGHTS["discount"] + (rating / 5.0) * WEIGHTS["rating"]
    if product.get("sponsorship", 0) == 1:
        base_score += WEIGHTS["boost"]
    return base_score

# ---------- SEARCH ----------
products = search_and_get_products(query)

if not products or "error" in products:
    st.warning("❌ No matching products found.")
    st.stop()

# ---------- BUILD PRODUCT LIST ----------
all_products = []
for pid, pdata in products.items():
    pdata["id"] = pid
    pdata["score"] = compute_score(pdata)
    pdata["price_value"] = pdata["price"].get("after_discount_price", 0)
    pdata["rating_value"] = pdata["sales"].get("avg_rating", 0)
    all_products.append(pdata)

# ---------- SORTING ----------
if sort_option == "Price: Low to High":
    sorted_products = sorted(all_products, key=lambda x: x["price_value"])
elif sort_option == "Price: High to Low":
    sorted_products = sorted(all_products, key=lambda x: x["price_value"], reverse=True)
elif sort_option == "Rating: High to Low":
    sorted_products = sorted(all_products, key=lambda x: x["rating_value"], reverse=True)
else:
    sorted_products = sorted(all_products, key=lambda x: x["score"], reverse=True)

# ---------- DISPLAY ----------
cols = st.columns(3)

for i, pdata in enumerate(sorted_products):
    pid = pdata["id"]
    with cols[i % 3]:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.image("./Image/images.png", use_container_width=True)

        if pdata.get("sponsorship", 0) == 1:
            st.markdown('<span style="color: green; font-weight: bold;">🎯 Sponsored Product</span>', unsafe_allow_html=True)

        st.subheader(pdata["details"].get("name", "Unnamed Product"))
        st.caption(pdata["details"].get("description", ""))

        st.markdown(f"💰 **Price:** ₹{pdata['price_value']}")
        st.markdown(f"🔻 **Discount:** {pdata['price'].get('discount', 0)}%")
        st.markdown(f"⭐ **Rating:** {pdata['rating_value']} / 5")

        if pdata["inventory"] == 0:
            st.markdown('<span style="color: red; font-weight: bold;">❌ Out of Stock</span>', unsafe_allow_html=True)
            st.button("🛒 Out of Stock", disabled=True, key=f"outofstock_{pid}")
        else:
            st.markdown(f"📦 **Stock Available:** {pdata['inventory']}")
            if st.button(f"🛒 Add to Cart - {pid}", key=f"addtocart_{pid}"):
                st.success(f"{pdata['details']['name']} added to cart!")

        st.markdown('</div>', unsafe_allow_html=True)

# ✅ Clear keyword
st.session_state.pop("keyword", None)
