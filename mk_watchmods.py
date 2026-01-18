import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.set_page_config(page_title="MK WATCH MODS", layout="wide")


# ---------------- EMAIL SENDER ----------------
def send_reservation_email(customer_name, customer_contact, model_name, collection_name):
    smtp_host = st.secrets["SMTP_HOST"]
    smtp_port = int(st.secrets["SMTP_PORT"])
    smtp_user = st.secrets["SMTP_USER"]
    smtp_pass = st.secrets["SMTP_PASS"]
    to_email = st.secrets["TO_EMAIL"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = f"[MK Watch Mods] New Reservation - {model_name}"
    body = f"""
NEW WATCH RESERVATION

Time: {now}
Collection: {collection_name}

Customer Name: {customer_name}
Customer Contact: {customer_contact}

Model Reserved: {model_name}
"""

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())


# ---------------- IMAGE NORMALIZER ----------------
def resize_square(img, size=700):
    w, h = img.size
    m = min(w, h)
    img = img.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
    return img.resize((size, size))


# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #f6f6f6; }
.main { background-color: #f6f6f6; }

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

.meta {
    color: #666;
    font-size: 14px;
    margin-top: 6px;
}
            
</style>
""", unsafe_allow_html=True)


# ---------------- DATA ----------------
custom_pieces = [
    {
        "id": "mystic_sea",
        "name": "Mystic Sea",
        "price": "$295",
        "imgs": [
            "images/mysticsea1.png",
            "images/mysticsea2.jpg",
            "images/mysticsea3.jpg",
        ],
        "diameter": "40mm",
        "thickness": "13.0mm",
        "lug_width": "20mm",
        "movement": "Seiko NH35 Automatic",
        "case_material": "Stainless Steel",
        "dial_color": "Blue",
        "bezel": "Unidirectional Dive Bezel",
        "water_resistance": "200m",
        "crystal": "Sapphire",
        "strap": "NATO (Blue/Grey)",
        "notes": "Custom-built Mod."
    },
]

homage = [
    {
        "id": "homage_diver_1",
        "name": "Homage Diver 1",
        "price": "$295",
        "imgs": [
            "images/watch4.jpg",
            "images/watch4_2.jpg",
        ],
        "diameter": "40mm",
        "thickness": "13.5mm",
        "lug_width": "20mm",
        "movement": "Seiko NH35 Automatic",
        "case_material": "Stainless Steel",
        "dial_color": "Blue",
        "bezel": "Unidirectional Dive Bezel",
        "water_resistance": "200m",
        "crystal": "Sapphire",
        "strap": "Bracelet",
        "notes": "Homage style build."
    },
    {
        "id": "homage_diver_2",
        "name": "Homage Diver 2",
        "price": "$295",
        "imgs": [
            "images/watch5.jpg",
            "images/watch5_2.jpg",
        ],
        "diameter": "40mm",
        "thickness": "13.5mm",
        "lug_width": "20mm",
        "movement": "Seiko NH35 Automatic",
        "case_material": "Stainless Steel",
        "dial_color": "Black",
        "bezel": "Unidirectional Dive Bezel",
        "water_resistance": "200m",
        "crystal": "Sapphire",
        "strap": "Bracelet",
        "notes": "Homage style build."
    },
    {
        "id": "homage_diver_3",
        "name": "Homage Diver 3",
        "price": "$295",
        "imgs": [
            "images/watch6.jpg",
            "images/watch6_2.jpg",
        ],
        "diameter": "40mm",
        "thickness": "13.5mm",
        "lug_width": "20mm",
        "movement": "Seiko NH35 Automatic",
        "case_material": "Stainless Steel",
        "dial_color": "Green",
        "bezel": "Unidirectional Dive Bezel",
        "water_resistance": "200m",
        "crystal": "Sapphire",
        "strap": "Bracelet",
        "notes": "Homage style build."
    },
]


# ---------------- STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "grid"  # grid | details

if "selected_watch_id" not in st.session_state:
    st.session_state.selected_watch_id = None

# Store carousel image index PER watch id
if "image_index" not in st.session_state:
    st.session_state.image_index = {}


# ---------------- HELPERS ----------------
def find_watch_by_id(watches, watch_id):
    for w in watches:
        if w["id"] == watch_id:
            return w
    return None


def get_watch_images(watch):
    img_list = watch.get("imgs", [])
    img_list = [p for p in img_list if p]
    return img_list


def get_current_img_path(watch):
    img_list = get_watch_images(watch)
    if len(img_list) == 0:
        return None

    if watch["id"] not in st.session_state.image_index:
        st.session_state.image_index[watch["id"]] = 0

    idx = st.session_state.image_index[watch["id"]]
    idx = max(0, min(idx, len(img_list) - 1))
    st.session_state.image_index[watch["id"]] = idx

    return img_list[idx]


def render_carousel(watch, image_size=700, show_caption=True, key_prefix=""):
    img_list = get_watch_images(watch)

    if len(img_list) == 0:
        st.error("No images found.")
        return

    if watch["id"] not in st.session_state.image_index:
        st.session_state.image_index[watch["id"]] = 0

    idx = st.session_state.image_index[watch["id"]]

    nav1, nav2, nav3 = st.columns([1, 6, 1])

    with nav1:
        if st.button("←", key=f"{key_prefix}prev_{watch['id']}"):
            st.session_state.image_index[watch["id"]] = (idx - 1) % len(img_list)
            st.rerun()

    with nav2:
        current_path = img_list[st.session_state.image_index[watch["id"]]]
        img = Image.open(current_path)
        img = resize_square(img, size=image_size)
        st.image(img, use_container_width=True)

        if show_caption:
            st.caption(f"Image {st.session_state.image_index[watch['id']] + 1} / {len(img_list)}")

    with nav3:
        if st.button("→", key=f"{key_prefix}next_{watch['id']}"):
            st.session_state.image_index[watch["id"]] = (idx + 1) % len(img_list)
            st.rerun()


def render_grid(watches, collection_name):
    cols = st.columns(3)

    for i, w in enumerate(watches):
        with cols[i % 3]:

            # One unified card container
            with st.container():
                st.markdown("""
                <div style="
                    background:white;
                    border-radius:20px;
                    padding:18px;
                    box-shadow:0 20px 40px rgba(0,0,0,0.06);
                    margin-bottom:18px;
                ">
                """, unsafe_allow_html=True)

                # Carousel
                render_carousel(w, image_size=700, show_caption=False, key_prefix="grid_")
                # Name + price + meta

                st.markdown(f"""
                    <div style="padding-top:10px;">
                        <h3 style="margin:0;">{w["name"]}</h3>
                        <div style="font-size:24px;font-weight:700;margin-top:6px;">{w["price"]}</div>
                        <div style="color:#666;font-size:14px;margin-top:6px;">
                            {w["movement"]} • {w["diameter"]} • {w["water_resistance"]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # Buttons INSIDE the card
                if st.button("View Details", use_container_width = True,key=f"details_{w['id']}"):
                    st.session_state.page = "details"
                    st.session_state.selected_watch_id = w["id"]
                    st.rerun()



                st.markdown("</div>", unsafe_allow_html=True)



def render_details(watch, collection_name):

    # TOP LEFT BACK BUTTON
    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button("← Back to Collection", key="back_to_grid_top"):
            st.session_state.page = "grid"
            st.session_state.selected_watch_id = None
            st.rerun()

    st.write("")  # small spacing

    top = st.columns([1, 1.2])

    with top[0]:
        render_carousel(watch, image_size=900, show_caption=True, key_prefix="details_")

    with top[1]:
        st.markdown(f"## {watch['name']}")
        st.markdown(f"### {watch['price']}")

        st.markdown("#### Specifications")
        st.markdown(f"""
- **Diameter:** {watch['diameter']}
- **Thickness:** {watch['thickness']}
- **Lug width:** {watch['lug_width']}
- **Movement:** {watch['movement']}
- **Case material:** {watch['case_material']}
- **Dial color:** {watch['dial_color']}
- **Bezel:** {watch['bezel']}
- **Crystal:** {watch['crystal']}
- **Water resistance:** {watch['water_resistance']}
- **Strap:** {watch['strap']}
""")

        if watch.get("notes"):
            st.info(watch["notes"])

        st.markdown("---")

        st.markdown("### Express Interest for this Piece")
        name = st.text_input("Your name", key="reserve_name")
        contact = st.text_input("Email or Handphone Number", key="reserve_contact")

        if st.button("Confirm Reservation", key="confirm_reserve"):
            if not name.strip():
                st.error("Please enter your name.")
                return
            if not contact.strip():
                st.error("Please enter your email or handphone number.")
                return

            contact_clean = contact.strip()
            is_email = ("@" in contact_clean) and ("." in contact_clean)
            is_phone = contact_clean.replace(" ", "").replace("-", "").replace("+", "").isdigit()

            if not (is_email or is_phone):
                st.error("Please enter a valid email or handphone number.")
                return

            try:
                send_reservation_email(
                    customer_name=name.strip(),
                    customer_contact=contact_clean,
                    model_name=watch["name"],
                    collection_name=collection_name
                )
                st.success(f"{name}, your {watch['name']} has been reserved. We will contact you shortly.")
            except Exception as e:
                st.error("Reservation recorded, but email failed to send.")
                st.code(str(e))

def trim_transparent(im):
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im

# ---------------- HERO ----------------
col1, col2, col3 = st.columns([1,1,1])

with col2:
    logo = Image.open("images/logo4.png")
    logo = trim_transparent(logo)
    st.image(logo, width=800)
#st.markdown("<div class='hero'>MK Watch Mods</div>", unsafe_allow_html=True)
    st.markdown(
    "<div class='subhero' style='text-align:center; font-style:italic; letter-spacing:1px;'>Automatic timepieces. For the love of the Art.</div>",
    unsafe_allow_html=True)
st.divider()


# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Custom Pieces", "Homage"],
        icons=["watch", "gem"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "12px",
                "background-color": "white",
                "border-radius": "18px",
                "box-shadow": "0 12px 30px rgba(0,0,0,0.08)"
            },
            "icon": {"color": "#111", "font-size": "13px"},
            "nav-link": {
                "font-size": "13px",
                "text-align": "left",
                "margin": "6px 0px",
                "color": "#111",
                "border-radius": "12px",
                "padding": "10px 12px",
            },
            "nav-link-selected": {
                "background-color": "#0B2D5B",  # dark blue
                "color": "white",
                "border-radius": "12px",
            },
        }
    )

collection_name = selected
watches = custom_pieces if selected == "Custom Pieces" else homage


# ---------------- PAGE RENDER ----------------
if st.session_state.page == "grid":
    render_grid(watches, collection_name)

elif st.session_state.page == "details":
    watch = find_watch_by_id(watches, st.session_state.selected_watch_id)

    if watch is None:
        st.session_state.page = "grid"
        st.session_state.selected_watch_id = None
        st.rerun()

    render_details(watch, collection_name)
