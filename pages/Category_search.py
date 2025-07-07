import streamlit as st
from utils.fetch_data import get_products

# ---------- CONFIG ----------
st.set_page_config(page_title="Category", layout="wide")

# ---------- CUSTOM CSS FOR CARD STYLING ----------
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



# ---------- WEIGHTS for Weighted Edge Ranking ----------
WEIGHTS = {
    "rating": 0.3,
    "discount": 0.2
}

# ---------- SCORE FUNCTION ----------
def compute_score(product, weights):
    inventory = product.get("inventory", 0)
    
    if inventory == 0:
        return -1  # bury out-of-stock

    score = 0
    rating = product["sales"].get("avg_rating", 0)
    score += (rating / 5.0) * weights["rating"]

    discount = product["price"].get("discount", 0)
    score += (discount / 100.0) * weights["discount"]

    return score

# ---------- GET SELECTED CATEGORY ----------
category = st.session_state.get("selected_category")
print("📌 Selected Category:", category)

if not category:
    st.warning("⚠️ No category selected.")
    st.stop()

st.title(f"🛍️ {category} Collection")

# ---------- FETCH PRODUCTS ----------
products = get_products(category)

if "error" in products:
    st.error(products["error"])
    st.stop()

print("📦 Products Fetched:")
sponsored_products = []
regular_products = []

# ---------- SPLIT PRODUCTS ----------
for pid, pdata in products.items():
    pdata["id"] = pid
    is_sponsored = pdata.get("sponsorship", 0) == 1

    if is_sponsored:
        sponsored_products.append(pdata)
        print(f" - {pid}: {pdata['details'].get('name')} (🎯 Sponsored)")
    else:
        pdata["score"] = compute_score(pdata, WEIGHTS)
        regular_products.append(pdata)
        print(f" - {pid}: {pdata['details'].get('name')} | Score: {pdata['score']:.2f}")

# ---------- SORT & COMBINE ----------
regular_products.sort(key=lambda x: x["score"], reverse=True)
final_product_list = sponsored_products + regular_products

# ---------- DISPLAY PRODUCTS IN 3 COLUMNS ----------
cols = st.columns(3)

for i, pdata in enumerate(final_product_list):
    pid = pdata["id"]
    with cols[i % 3]:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        st.image("./Image/images.png", use_container_width=True)


        # 🎯 Sponsored badge
        if pdata.get("sponsorship", 0) == 1:
            st.markdown('<span style="color: green; font-weight: bold;">🎯 Sponsored Product</span>', unsafe_allow_html=True)

        st.subheader(pdata["details"].get("name", "Unnamed Product"))
        st.caption(pdata["details"].get("description", ""))

        st.markdown(f"💰 **Price:** ₹{pdata['price'].get('after_discount_price', 'N/A')}")
        st.markdown(f"🔻 **Discount:** {pdata['price'].get('discount', 0)}%")
        st.markdown(f"⭐ **Rating:** {pdata['sales'].get('avg_rating', 0)} / 5")

        if pdata["inventory"] == 0:
            st.markdown('<span style="color: red; font-weight: bold;">❌ Out of Stock</span>', unsafe_allow_html=True)
            st.button(f"🛒 Out of Stock", disabled=True)
        else:
            st.markdown(f"📦 **Stock Available:** {pdata['inventory']}")
            if st.button(f"🛒 Add to Cart - {pid}"):
                st.success(f"{pdata['details']['name']} added to cart!")

        st.markdown('</div>', unsafe_allow_html=True)
