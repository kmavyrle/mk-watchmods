import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

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

/* Tab styling */
button[data-baseweb="tab"] {
    font-size: 18px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #888 !important;
    padding: 12px 32px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #0B2D5B !important;
    border-bottom: 3px solid #0B2D5B !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: #0B2D5B !important;
}

div[data-baseweb="tab-border"] {
    background-color: #ddd !important;
}

button[data-baseweb="tab"]:hover {
    color: #0B2D5B !important;
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
        "water_resistance": "Do not dive with watch",
        "crystal": "Sapphire",
        "strap": "NATO (Blue/Grey)",
        "notes": "Custom-built Mod."
    },
]

homage = [
    {
        "id": "RHM",
        "name": "Seiko Hulk Mod",
        "price": "$250",
        "imgs": [
            "images/seikohulkmod1.png",
            "images/mod1.jpg",
        ],
        "diameter": "40mm",
        "thickness": "13.5mm",
        "lug_width": "20mm",
        "movement": "Seiko NH35 Automatic",
        "case_material": "Stainless Steel",
        "dial_color": "Green",
        "bezel": "Unidirectional Dive Bezel",
        "water_resistance": "Do not dive with watch",
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
                    background:var(--secondary-background-color);
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
                if st.button("View", use_container_width = True,key=f"details_{w['id']}"):
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

        if st.button("Confirm", key="confirm_reserve"):
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
                st.success(f"{name}, your interest in {watch['name']} has acknowledged. We will contact you shortly.")
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
    "<div class='subhero' style='text-align:center; font-style:italic; letter-spacing:1px;'>Automatic timepieces. Made with care.</div>",
    unsafe_allow_html=True)
st.divider()

# ---------------- MINI GAME ----------------
GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:transparent; display:flex; flex-direction:column; align-items:center; }
canvas { display:block; border-radius:14px; cursor:pointer; }
</style>
</head>
<body>
<canvas id="c" width="860" height="160"></canvas>
<script>
const c = document.getElementById('c');
const ctx = c.getContext('2d');
const W = c.width, H = c.height;
const GROUND = H - 28;
const PX = 90, PW = 22, PH = 30;

let state = 'idle', score = 0, hi = 0, speed = 5, frame = 0, raf;
const p = { y: GROUND - PH, vy: 0, jumping: false };
let obs = [];

function reset() {
    p.y = GROUND - PH; p.vy = 0; p.jumping = false;
    obs = []; score = 0; speed = 5; frame = 0;
    state = 'running';
    cancelAnimationFrame(raf);
    loop();
}

function tryJump() {
    if (state !== 'running') { reset(); return; }
    if (!p.jumping) { p.vy = -14; p.jumping = true; }
}

function loop() {
    raf = requestAnimationFrame(loop);
    frame++; score++;
    speed = 5 + score / 300;

    p.vy += 0.75; p.y += p.vy;
    if (p.y >= GROUND - PH) { p.y = GROUND - PH; p.vy = 0; p.jumping = false; }

    const interval = Math.max(55, 90 - Math.floor(score / 100));
    if (frame % interval === 0) {
        obs.push({ x: W + 10, w: 10 + Math.random() * 10, h: 18 + Math.random() * 28 });
    }
    obs.forEach(o => o.x -= speed);
    obs = obs.filter(o => o.x > -30);

    for (const o of obs) {
        if (PX + PW - 4 > o.x && PX + 4 < o.x + o.w &&
            p.y + PH - 4 > GROUND - o.h && p.y + 4 < GROUND) {
            hi = Math.max(hi, score);
            state = 'dead';
            cancelAnimationFrame(raf);
            draw(); return;
        }
    }
    draw();
}

function draw() {
    ctx.fillStyle = '#0d1117';
    ctx.beginPath(); ctx.roundRect(0, 0, W, H, 14); ctx.fill();

    ctx.fillStyle = '#1a3a6b';
    ctx.fillRect(0, GROUND, W, 2);

    // Player watch body
    ctx.fillStyle = '#2a6dd9';
    ctx.beginPath(); ctx.roundRect(PX, p.y, PW, PH, 5); ctx.fill();
    ctx.fillStyle = '#1a4a99';
    ctx.fillRect(PX + 5, p.y - 5, PW - 10, 5);
    ctx.fillRect(PX + 5, p.y + PH, PW - 10, 5);
    ctx.strokeStyle = '#a0c4ff'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(PX + PW/2, p.y + PH/2, 8, 0, Math.PI*2); ctx.stroke();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(PX+PW/2, p.y+PH/2); ctx.lineTo(PX+PW/2, p.y+PH/2-5); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(PX+PW/2, p.y+PH/2); ctx.lineTo(PX+PW/2+4, p.y+PH/2); ctx.stroke();

    // Obstacles
    obs.forEach(o => {
        ctx.fillStyle = '#c0392b';
        ctx.beginPath(); ctx.roundRect(o.x, GROUND-o.h, o.w, o.h, 3); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.12)';
        ctx.fillRect(o.x+2, GROUND-o.h+2, 2, o.h-4);
    });

    // Score
    ctx.fillStyle = '#4a7fbd'; ctx.font = 'bold 13px monospace'; ctx.textAlign = 'right';
    ctx.fillText('HI ' + String(hi).padStart(5,'0') + '   ' + String(score).padStart(5,'0'), W-18, 26);

    ctx.textAlign = 'center';
    if (state === 'idle') {
        ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.font = '13px monospace';
        ctx.fillText('CLICK  OR  SPACE  TO  PLAY', W/2, H/2+6);
    }
    if (state === 'dead') {
        ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.font = 'bold 15px monospace';
        ctx.fillText('GAME  OVER', W/2, H/2-6);
        ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.font = '11px monospace';
        ctx.fillText('click or space to restart', W/2, H/2+14);
    }
}

draw();
c.addEventListener('click', tryJump);
window.addEventListener('keydown', e => {
    if (e.code === 'Space' || e.code === 'ArrowUp') { e.preventDefault(); tryJump(); }
});
</script>
</body>
</html>
"""

with st.expander("🎮 bored? play a game", expanded=False):
    components.html(GAME_HTML, height=180)

st.divider()

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Custom Pieces", "Homage"])

with tab1:
    collection_name = "Custom Pieces"
    watches = custom_pieces
    if st.session_state.page == "grid":
        render_grid(watches, collection_name)
    elif st.session_state.page == "details":
        watch = find_watch_by_id(watches, st.session_state.selected_watch_id)
        if watch:
            render_details(watch, collection_name)
        else:
            render_grid(watches, collection_name)

with tab2:
    collection_name = "Homage"
    watches = homage
    if st.session_state.page == "grid":
        render_grid(watches, collection_name)
    elif st.session_state.page == "details":
        watch = find_watch_by_id(watches, st.session_state.selected_watch_id)
        if watch:
            render_details(watch, collection_name)
        else:
            render_grid(watches, collection_name)
