import streamlit as st
from utils.offer_products import get_offered_products

# ---------- CONFIG ----------
st.set_page_config(page_title="Offers", layout="wide")

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

st.title("🔥 Limited Time Offers")

# ---------- FETCH PRODUCTS ----------
products = get_offered_products()

if "error" in products:
    st.error(products["error"])
    st.stop()

# ---------- SCORING WEIGHTS ----------
WEIGHTS = {
    "discount": 0.7,
    "rating": 0.3
}

# ---------- SCORE FUNCTION ----------
def compute_offer_score(product):
    if product.get("inventory", 0) == 0:
        return -1
    discount = product["price"].get("discount", 0)
    rating = product["sales"].get("avg_rating", 0)
    score = (discount / 100.0) * WEIGHTS["discount"]
    score += (rating / 5.0) * WEIGHTS["rating"]
    return score

# ---------- CLASSIFY & SCORE ----------
sponsored_instock = []
regular_instock = []
out_of_stock = []

for pid, pdata in products.items():
    pdata["id"] = pid
    is_sponsored = pdata.get("sponsorship", 0) == 1
    inventory = pdata.get("inventory", 0)

    if inventory == 0:
        out_of_stock.append(pdata)
    elif is_sponsored:
        sponsored_instock.append(pdata)
    else:
        pdata["score"] = compute_offer_score(pdata)
        regular_instock.append(pdata)

# ---------- SORT REGULAR PRODUCTS BY SCORE ----------
regular_instock.sort(key=lambda x: x["score"], reverse=True)

# ---------- FINAL PRODUCT LIST ----------
final_products = sponsored_instock + regular_instock + out_of_stock

# ---------- DISPLAY PRODUCTS IN 3 COLUMNS ----------
cols = st.columns(3)

for i, pdata in enumerate(final_products):
    pid = pdata["id"]
    with cols[i % 3]:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)

        st.image("./Image/images.png", use_container_width=True)

        if pdata.get("sponsorship", 0) == 1:
            st.markdown('<span style="color: green; font-weight: bold;">🎯 Sponsored Product</span>', unsafe_allow_html=True)

        st.subheader(pdata["details"].get("name", "Unnamed Product"))
        st.caption(pdata["details"].get("description", ""))

        st.markdown(f"💰 **Price:** ₹{pdata['price'].get('after_discount_price', 'N/A')}")
        st.markdown(f"🔻 **Discount:** {pdata['price'].get('discount', 0)}%")
        st.markdown(f"⭐ **Rating:** {pdata['sales'].get('avg_rating', 0)} / 5")

        if pdata.get("inventory", 0) == 0:
            st.markdown('<span style="color: red; font-weight: bold;">❌ Out of Stock</span>', unsafe_allow_html=True)
            st.button("🛒 Out of Stock", disabled=True, key=f"outofstock_{pid}")
        else:
            st.markdown(f"📦 **Stock Available:** {pdata['inventory']}")
            if st.button(f"🛒 Add to Cart - {pid}", key=f"addtocart_{pid}"):
                st.success(f"{pdata['details']['name']} added to cart!")

        st.markdown('</div>', unsafe_allow_html=True)
