import streamlit as st
from PIL import Image

st.set_page_config(page_title="MAVYRLE", layout="wide")

# ---------------- IMAGE NORMALIZER ----------------
def resize_square(img, size=700):
    w, h = img.size
    m = min(w, h)
    img = img.crop(((w-m)//2, (h-m)//2, (w+m)//2, (h+m)//2))
    return img.resize((size, size))

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f6f6f6;
}
.main {
    background-color: #f6f6f6;
}
.hero {
    font-size: 70px;
    font-weight: 800;
    letter-spacing: -2px;
    color: #111;
}
.subhero {
    font-size: 22px;
    color: #666;
    margin-bottom: 40px;
}
.card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.06);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 30px 60px rgba(0,0,0,0.12);
}
.price {
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
}
.buy {
    background: #111;
    color: white;
    padding: 12px;
    border-radius: 10px;
    text-align:center;
    font-weight: 600;
    margin-top: 15px;
}
.buy:hover {
    background: black;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("<div class='hero'>MK Watch Mods</div>", unsafe_allow_html=True)
st.markdown("<div class='subhero'>High-Performance Automatic Timepieces</div>", unsafe_allow_html=True)

st.divider()

# ---------------- PRODUCTS ----------------
watches = [
    {"name":"Mystic Sea 1", "price":"$295", "img":"images/watch1.jpg"},
    {"name":"Mystic Sea 2", "price":"$295", "img":"images/watch2.jpg"},
    {"name":"Mystic Sea 3", "price":"$295", "img":"images/watch3.jpg"},
]

cols = st.columns(3)

for i, w in enumerate(watches):
    with cols[i]:
        img = Image.open(w["img"])
        img = resize_square(img)
        st.image(img, use_container_width=True)
        st.markdown(f"""
        <div class="card">
            <h3>{w["name"]}</h3>
            <div class="price">{w["price"]}</div>
            <div class="buy">Reserve</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()



st.divider()

# ---------------- RESERVATION ----------------
st.markdown("## Reserve a Watch")

name = st.text_input("Your name")
email = st.text_input("Email")
model = st.selectbox("Select model", [w["name"] for w in watches])

if st.button("Reserve"):
    st.success(f"{name}, your {model} has been reserved. We will contact you shortly.")
