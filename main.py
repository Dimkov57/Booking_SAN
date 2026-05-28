import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import hashlib, re
import db

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="UniRoom — Room Booking",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f1117;
    color: #e8e4dc;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161922;
    border-right: 1px solid #2a2f3e;
}
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 60%, #1e1530 100%);
    border: 1px solid #2a2f3e;
    border-radius: 16px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(130,80,255,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.3rem;
    color: #f0ebe0;
    margin: 0 0 0.35rem;
    letter-spacing: -0.5px;
}
.hero p   { color: #9896a0; font-size: 1rem; margin: 0; font-weight: 300; }
.hero .badge {
    display: inline-block;
    background: rgba(130,80,255,0.15);
    border: 1px solid rgba(130,80,255,0.4);
    color: #a97eff;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.73rem; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 0.7rem;
}

/* ── Avatar chip (sidebar) ── */
.avatar-chip {
    display: flex; align-items: center; gap: 10px;
    background: #1e2333; border: 1px solid #2a2f3e;
    border-radius: 10px; padding: 0.7rem 1rem;
    margin-bottom: 1.2rem;
}
.avatar-circle {
    width: 36px; height: 36px; border-radius: 50%;
    background: linear-gradient(135deg, #8250ff, #5030c8);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; color: #fff; font-weight: 600; flex-shrink: 0;
}
.avatar-info .name  { font-size: 0.88rem; color: #e8e4dc; font-weight: 500; line-height: 1.2; }
.avatar-info .sid   { font-size: 0.75rem; color: #6e6c78; }

/* ── Cards ── */
.room-card {
    background: #161922; border: 1px solid #2a2f3e;
    border-radius: 12px; padding: 1.3rem 1.5rem; margin-bottom: 0.9rem;
}
.room-card h3 { font-family: 'Playfair Display', serif; font-size: 1.15rem; margin: 0 0 0.25rem; color: #f0ebe0; }
.room-card .meta { color: #7a7880; font-size: 0.83rem; margin: 0; }
.tag         { display:inline-block; background:rgba(80,160,255,0.1);  border:1px solid rgba(80,160,255,0.3);  color:#50a0ff;  padding:2px 10px; border-radius:20px; font-size:0.71rem; margin:6px 4px 0 0; }
.tag.lab     { background:rgba(80,220,160,0.1); border-color:rgba(80,220,160,0.3); color:#50dca0; }
.tag.hall    { background:rgba(255,160,60,0.1); border-color:rgba(255,160,60,0.3); color:#ffa03c; }

/* ── Booking tile ── */
.booking-tile {
    background: #161922; border-left: 3px solid #8250ff;
    border-radius: 0 10px 10px 0; padding: 0.85rem 1.15rem; margin-bottom: 0.65rem;
}
.booking-tile h4 { margin: 0 0 0.2rem; font-size: 0.98rem; color: #f0ebe0; }
.booking-tile p  { margin: 0; font-size: 0.81rem; color: #9896a0; }

/* ── Pills ── */
.pill-free  { color:#50dca0; background:rgba(80,220,160,0.1);  border:1px solid rgba(80,220,160,0.3);  border-radius:20px; padding:2px 12px; font-size:0.77rem; }
.pill-taken { color:#ff6b6b; background:rgba(255,107,107,0.1); border:1px solid rgba(255,107,107,0.3); border-radius:20px; padding:2px 12px; font-size:0.77rem; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #8250ff, #5030c8) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important; padding: 0.5rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Inputs ── */
.stSelectbox > div > div,
.stDateInput > div > div > input,
.stTextInput > div > div > input {
    background: #1e2333 !important; border: 1px solid #2a2f3e !important;
    color: #e8e4dc !important; border-radius: 8px !important;
}

hr { border-color: #2a2f3e; }

[data-testid="metric-container"] {
    background: #161922; border: 1px solid #2a2f3e;
    border-radius: 10px; padding: 1rem 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROOM CATALOGUE
# ══════════════════════════════════════════════════════════════════════════════
ROOMS = {
    "P11": {"capacity": 120, "type": "hall",    "floor": 1, "amenities": ["Projector", "Microphone", "AC"]},
    "P12": {"capacity": 30,  "type": "lab",     "floor": 1, "amenities": ["Whiteboard", "TV Screen"]},
    "P13": {"capacity": 30,  "type": "study",   "floor": 1, "amenities": ["40 PCs", "Projector", "AC"]},
    "P21": {"capacity": 20,  "type": "seminar", "floor": 2, "amenities": ["Whiteboard", "WiFi"]},
    "P22": {"capacity": 30,  "type": "lab",     "floor": 2, "amenities": ["Whiteboard", "WiFi"]},
    "P23": {"capacity": 30,  "type": "study",   "floor": 2, "amenities": ["Video conferencing", "Projector", "AC"]},
    "P31": {"capacity": 20,  "type": "seminar", "floor": 3, "amenities": ["Drawing tablets", "Large screens"]},
    "P32": {"capacity": 30,  "type": "lab",     "floor": 3, "amenities": ["Stage", "Full AV", "AC", "Streaming"]},
    "P33": {"capacity": 30,  "type": "study",   "floor": 3, "amenities": ["Stage", "Full AV", "AC", "Streaming"]},
    "K11": {"capacity": 30,  "type": "seminar", "floor": 1, "amenities": ["Projector", "Microphone", "AC"]},
    "K12": {"capacity": 30,  "type": "lab",     "floor": 1, "amenities": ["Whiteboard", "TV Screen"]},
    "K13": {"capacity": 30,  "type": "seminar", "floor": 1, "amenities": ["40 PCs", "Projector", "AC"]},
    "K21": {"capacity": 30,  "type": "study",   "floor": 2, "amenities": ["Whiteboard", "WiFi"]},
    "K22": {"capacity": 30,  "type": "lab",     "floor": 2, "amenities": ["Whiteboard", "WiFi"]},
    "K23": {"capacity": 30,  "type": "study",   "floor": 2, "amenities": ["Video conferencing", "Projector", "AC"]},
    "K31": {"capacity": 30,  "type": "seminar", "floor": 3, "amenities": ["Drawing tablets", "Large screens"]},
    "K32": {"capacity": 30,  "type": "lab",     "floor": 3, "amenities": ["Stage", "Full AV", "AC", "Streaming"]},
    "K33": {"capacity": 30,  "type": "study",   "floor": 3, "amenities": ["Stage", "Full AV", "AC", "Streaming"]},
}

TIME_SLOTS = [
    "08:00-09:30", "09:45-11:15", "11:30-13:00",
    "13:15-14:45", "15:00-16:30", "16:45-18:15", "18:30-20:15",
]

TAG_COLORS = {
    "hall": "tag hall", "lab": "tag lab",
    "seminar": "tag", "study": "tag",
}

FACULTIES = [
    "Computer Science", "Mathematics", "Physics", "Chemistry",
    "Biology", "Economics", "Law", "Humanities", "Engineering", "Other",
]

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
if "bookings"     not in st.session_state: st.session_state.bookings     = db.get_all_bookings()
if "users"        not in st.session_state: st.session_state.users        = db.get_all_users()
if "logged_in"    not in st.session_state: st.session_state.logged_in    = False
if "current_user" not in st.session_state: st.session_state.current_user = None

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
MAX_SEATS = 30

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def validate_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", email))

def user_initials(name: str) -> str:
    parts = name.strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else name[:2].upper()

def current_user_data() -> dict:
    return st.session_state.users.get(st.session_state.current_user, {})

def get_slot_bookings(room: str, booking_date: str, slot: str) -> list:
    return [
        b for b in st.session_state.bookings
        if b["room"] == room and b["date"] == booking_date and b["slot"] == slot
    ]

def slot_seats_taken(room: str, booking_date: str, slot: str) -> int:
    return len(get_slot_bookings(room, booking_date, slot))

def is_slot_full(room: str, booking_date: str, slot: str) -> bool:
    return slot_seats_taken(room, booking_date, slot) >= MAX_SEATS

def user_already_booked(room: str, booking_date: str, slot: str, student_id: str) -> bool:
    return any(b["student_id"] == student_id for b in get_slot_bookings(room, booking_date, slot))

def get_room_bookings(room: str, booking_date: str) -> list:
    return [b for b in st.session_state.bookings if b["room"] == room and b["date"] == booking_date]

def reload_state():
    """Re-fetch both users and bookings from the DB into session state."""
    st.session_state.users    = db.get_all_users()
    st.session_state.bookings = db.get_all_bookings()

# ══════════════════════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════════════════════
def show_auth():
    st.markdown("""
    <div style='text-align:center; margin: 2.5rem 0 1.5rem'>
        <div style='font-family:"Playfair Display",serif; font-size:2.4rem; color:#f0ebe0; letter-spacing:-1px'>
            🏛️ UniRoom
        </div>
        <div style='color:#6e6c78; font-size:0.92rem; margin-top:6px'>
            University Room Booking System
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        tab_login, tab_reg = st.tabs(["Sign In", "Create Account"])

        # ── Login ──────────────────────────────────────────────────────────────
        with tab_login:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            sid = st.text_input("Student ID", placeholder="e.g. s12345", key="li_sid")
            pw  = st.text_input("Password",   type="password",           key="li_pw")
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
            if st.button("Sign In  →", use_container_width=True, key="li_btn"):
                users = st.session_state.users
                if not sid or not pw:
                    st.error("Please fill in all fields.")
                elif sid not in users:
                    st.error("Student ID not found. Please register first.")
                elif users[sid]["password"] != hash_password(pw):
                    st.error("Incorrect password.")
                else:
                    st.session_state.logged_in    = True
                    st.session_state.current_user = sid
                    st.rerun()

        # ── Register ───────────────────────────────────────────────────────────
        with tab_reg:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            r1, r2  = st.columns(2)
            first   = r1.text_input("First Name", key="reg_fn")
            last    = r2.text_input("Last Name",  key="reg_ln")
            email   = st.text_input("University Email", placeholder="name@university.edu", key="reg_email")
            sid_r   = st.text_input("Student ID",       placeholder="e.g. s12345",         key="reg_sid")
            faculty = st.selectbox("Faculty", FACULTIES, key="reg_fac")
            pw1     = st.text_input("Password",         type="password", key="reg_pw1")
            pw2     = st.text_input("Confirm Password", type="password", key="reg_pw2")
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

            if st.button("Create Account  →", use_container_width=True, key="reg_btn"):
                users = st.session_state.users
                err   = None
                if not all([first, last, email, sid_r, pw1, pw2]):
                    err = "Please fill in all fields."
                elif not validate_email(email):
                    err = "Please enter a valid email address."
                elif sid_r in users:
                    err = "This Student ID is already registered."
                elif len(pw1) < 6:
                    err = "Password must be at least 6 characters."
                elif pw1 != pw2:
                    err = "Passwords do not match."

                if err:
                    st.error(err)
                else:
                    ok = db.create_user(
                        student_id    = sid_r.strip(),
                        first_name    = first.strip(),
                        last_name     = last.strip(),
                        email         = email.strip().lower(),
                        faculty       = faculty,
                        password_hash = hash_password(pw1),
                        joined        = datetime.now().strftime("%Y-%m-%d"),
                    )
                    if ok:
                        reload_state()
                        st.session_state.logged_in    = True
                        st.session_state.current_user = sid_r.strip()
                        st.success("Account created! Welcome to UniRoom!")
                        st.rerun()
                    else:
                        st.error("Registration failed — Student ID or email already exists.")

# ══════════════════════════════════════════════════════════════════════════════
# GATE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_auth()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
u = current_user_data()

with st.sidebar:
    initials = user_initials(u.get("name", "?"))
    st.markdown(f"""
    <div class="avatar-chip">
        <div class="avatar-circle">{initials}</div>
        <div class="avatar-info">
            <div class="name">{u.get('name','')}</div>
            <div class="sid">{u.get('student_id','')} &middot; {u.get('faculty','')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["📅 Book a Room", "📋 My Bookings", "👤 My Profile", "🗺️ Room Overview", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='margin:1.2rem 0 0.8rem'>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in    = False
        st.session_state.current_user = None
        st.rerun()

    st.markdown(
        "<div style='font-size:0.75rem;color:#4a4858;margin-top:0.8rem;line-height:1.7'>"
        "UniRoom &middot; Academic Year 2025/26</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — BOOK A ROOM
# ══════════════════════════════════════════════════════════════════════════════
if page == "📅 Book a Room":
    st.markdown(f"""
    <div class="hero">
        <div class="badge">Book</div>
        <h1>Reserve Your Space</h1>
        <p>Hello, <b style="color:#e8e4dc">{u.get('first_name','')}</b> — find and book a room in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_info = st.columns([1.3, 1], gap="large")

    with col_form:
        st.markdown("#### Booking Details")
        purpose       = st.text_input("Purpose / Group Name", placeholder="e.g. Study group — Data Science")
        selected_room = st.selectbox("Select Room", list(ROOMS.keys()))
        selected_date = st.date_input(
            "Date",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=30),
        )
        date_str    = str(selected_date)
        avail_slots = [s for s in TIME_SLOTS if not is_slot_full(selected_room, date_str, s)]

        if avail_slots:
            selected_slot = st.selectbox(
                "Time Slot",
                avail_slots,
                format_func=lambda s: (
                    f"{s}  \u2014  {MAX_SEATS - slot_seats_taken(selected_room, date_str, s)}/{MAX_SEATS} seats free"
                ),
            )
        else:
            st.error("All slots for this room are fully booked on the selected date.")
            selected_slot = None

        st.markdown("")
        if st.button("Confirm Booking", use_container_width=True):
            if not selected_slot:
                st.error("No available slots.")
            elif user_already_booked(selected_room, date_str, selected_slot, u["student_id"]):
                st.error("You already have a booking for this room, date and time slot.")
            elif is_slot_full(selected_room, date_str, selected_slot):
                st.error("This slot just filled up. Please choose another.")
            else:
                booking = {
                    "id":         f"{u['student_id']}-{date_str}-{selected_slot[:5]}-{int(datetime.now().timestamp())}",
                    "name":       u["name"],
                    "student_id": u["student_id"],
                    "email":      u["email"],
                    "faculty":    u["faculty"],
                    "purpose":    purpose.strip() or "Not specified",
                    "room":       selected_room,
                    "date":       date_str,
                    "slot":       selected_slot,
                    "booked_at":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                ok = db.add_booking(booking)
                if ok:
                    st.session_state.bookings = db.get_all_bookings()  
                    st.rerun()  
                    taken_now = slot_seats_taken(selected_room, date_str, selected_slot)
                    st.success(
                        f"Booked **{selected_room}** on **{date_str}** at **{selected_slot}**!  "
                        f"({taken_now}/{MAX_SEATS} seats taken)"
                    )
                    st.balloons()
                else:
                    st.error("Booking failed — slot may have just been taken. Please try again.")

    with col_info:
        st.markdown("#### Room Info")
        info    = ROOMS[selected_room]
        tag_cls = TAG_COLORS.get(info["type"], "tag")
        amenity_tags = "".join(f'<span class="tag">{a}</span>' for a in info["amenities"])
        st.markdown(f"""
        <div class="room-card">
            <h3>{selected_room}</h3>
            <p class="meta">Floor {info['floor']} &nbsp;&middot;&nbsp; Capacity: {info['capacity']} people</p>
            <span class="{tag_cls}">{info['type'].upper()}</span>
            <br>{amenity_tags}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"#### Availability for {date_str}")
        for slot in TIME_SLOTS:
            taken_n   = slot_seats_taken(selected_room, date_str, slot)
            full      = taken_n >= MAX_SEATS
            if full:
                pill = '<span class="pill-taken">Full</span>'
            elif taken_n == 0:
                pill = '<span class="pill-free">Free</span>'
            else:
                pill = f'<span class="pill-free">{MAX_SEATS - taken_n} left</span>'
            bar_pct   = int(taken_n / MAX_SEATS * 100)
            bar_color = "#ff6b6b" if full else ("#f0a040" if taken_n > MAX_SEATS * 0.7 else "#50dca0")
            st.markdown(
                f"<div style='padding:0.42rem 0;border-bottom:1px solid #1e2333'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                f"<span style='font-size:0.86rem;color:#ccc'>{slot}</span>{pill}</div>"
                f"<div style='background:#1e2333;border-radius:4px;height:4px;margin-top:5px'>"
                f"<div style='background:{bar_color};width:{bar_pct}%;height:4px;border-radius:4px'></div>"
                f"</div><div style='font-size:0.72rem;color:#6e6c78;margin-top:3px'>{taken_n}/{MAX_SEATS} seats taken</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — MY BOOKINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 My Bookings":
    st.markdown(f"""
    <div class="hero">
        <div class="badge">History</div>
        <h1>My Bookings</h1>
        <p>All reservations for <b style="color:#e8e4dc">{u.get('name','')}</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    my_bookings = sorted(
        [b for b in st.session_state.bookings if b["student_id"] == u["student_id"]],
        key=lambda x: (x["date"], x["slot"]),
    )
    today_str = str(date.today())
    upcoming  = [b for b in my_bookings if b["date"] >= today_str]
    past      = [b for b in my_bookings if b["date"] <  today_str]

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Bookings", len(my_bookings))
    m2.metric("Upcoming",       len(upcoming))
    m3.metric("Past",           len(past))
    st.markdown("---")

    def render_bookings(items, allow_cancel):
        if not items:
            st.markdown(
                "<div style='color:#6e6c78;font-size:0.9rem;padding:0.5rem 0'>Nothing here yet.</div>",
                unsafe_allow_html=True,
            )
            return
        for b in items:
            col_tile, col_btn = st.columns([5, 1])
            with col_tile:
                st.markdown(f"""
                <div class="booking-tile">
                    <h4>{b['room']}</h4>
                    <p>📅 {b['date']} &nbsp;&middot;&nbsp; ⏰ {b['slot']}</p>
                    <p>📝 {b['purpose']} &nbsp;&middot;&nbsp; 🕐 Booked: {b.get('booked_at','—')}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if allow_cancel:
                    if st.button("Cancel", key=f"cancel-{b['id']}"):
                        db.cancel_booking(b["id"])
                        st.session_state.bookings = db.get_all_bookings()
                        st.rerun()

    tab_up, tab_past = st.tabs(["Upcoming", "Past"])
    with tab_up:   render_bookings(upcoming, allow_cancel=True)
    with tab_past: render_bookings(past,     allow_cancel=False)

    if my_bookings:
        st.markdown("---")
        csv = pd.DataFrame(my_bookings).to_csv(index=False).encode()
        st.download_button("Export as CSV", csv, "my_bookings.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — MY PROFILE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👤 My Profile":
    st.markdown("""
    <div class="hero">
        <div class="badge">Account</div>
        <h1>My Profile</h1>
        <p>Manage your personal information and password.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_info, tab_pass = st.tabs(["Personal Info", "Change Password"])

    # ── Personal Info tab ──────────────────────────────────────────────────────
    with tab_info:
        col_av, col_data = st.columns([1, 2.5], gap="large")

        with col_av:
            initials = user_initials(u.get("name", "?"))
            st.markdown(f"""
            <div style='text-align:center; padding:1.5rem 0'>
                <div style='width:88px;height:88px;border-radius:50%;
                    background:linear-gradient(135deg,#8250ff,#5030c8);
                    display:flex;align-items:center;justify-content:center;
                    font-size:2rem;color:#fff;font-weight:700;margin:0 auto 1rem'>
                    {initials}
                </div>
                <div style='font-family:"Playfair Display",serif;font-size:1.15rem;color:#f0ebe0'>
                    {u.get('name','')}
                </div>
                <div style='font-size:0.78rem;color:#6e6c78;margin-top:5px'>
                    Student since {u.get('joined','—')}
                </div>
                <div style='font-size:0.78rem;color:#6e6c78;margin-top:3px'>
                    {u.get('email','')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_data:
            st.markdown("#### Edit Profile")
            new_first   = st.text_input("First Name", value=u.get("first_name", ""), key="pf_fn")
            new_last    = st.text_input("Last Name",  value=u.get("last_name",  ""), key="pf_ln")
            new_email   = st.text_input("Email",      value=u.get("email",      ""), key="pf_em")
            fac_index   = FACULTIES.index(u.get("faculty", "Other")) if u.get("faculty") in FACULTIES else 0
            new_faculty = st.selectbox("Faculty", FACULTIES, index=fac_index, key="pf_fac")

            st.markdown("")
            if st.button("Save Changes", use_container_width=True, key="pf_save"):
                if not new_first or not new_last:
                    st.error("Name fields cannot be empty.")
                elif not validate_email(new_email):
                    st.error("Invalid email address.")
                else:
                    uid = st.session_state.current_user
                    db.update_user(
                        student_id = uid,
                        first_name = new_first.strip(),
                        last_name  = new_last.strip(),
                        email      = new_email.strip().lower(),
                        faculty    = new_faculty,
                    )
                    reload_state()
                    st.success("Profile updated successfully!")
                    st.rerun()

        st.markdown("---")
        my_b      = [b for b in st.session_state.bookings if b["student_id"] == u["student_id"]]
        today_str = str(date.today())
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Bookings", len(my_b))
        s2.metric("Upcoming",       len([b for b in my_b if b["date"] >= today_str]))
        s3.metric("Unique Rooms",   len({b["room"] for b in my_b}))

    # ── Change Password tab ────────────────────────────────────────────────────
    with tab_pass:
        col_pw, _ = st.columns([1.5, 1])
        with col_pw:
            st.markdown("#### Change Password")
            old_pw  = st.text_input("Current Password",     type="password", key="cp_old")
            new_pw1 = st.text_input("New Password",         type="password", key="cp_new1")
            new_pw2 = st.text_input("Confirm New Password", type="password", key="cp_new2")
            st.markdown("")
            if st.button("Update Password", use_container_width=True, key="cp_btn"):
                uid = st.session_state.current_user
                if st.session_state.users[uid]["password"] != hash_password(old_pw):
                    st.error("Current password is incorrect.")
                elif len(new_pw1) < 6:
                    st.error("New password must be at least 6 characters.")
                elif new_pw1 != new_pw2:
                    st.error("Passwords do not match.")
                else:
                    db.update_password(uid, hash_password(new_pw1))
                    reload_state()
                    st.success("Password updated successfully!")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — ROOM OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Room Overview":
    st.markdown("""
    <div class="hero">
        <div class="badge">Browse</div>
        <h1>All Rooms</h1>
        <p>Explore available spaces across all floors.</p>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    filter_type     = f1.selectbox("Type", ["All"] + sorted({r["type"] for r in ROOMS.values()}))
    filter_capacity = f2.slider("Min. Capacity", 1, 300, 1)
    filter_date     = f3.date_input(
        "Check availability on",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=30),
    )
    date_str = str(filter_date)

    for room_name, info in ROOMS.items():
        if filter_type != "All" and info["type"] != filter_type:
            continue
        if info["capacity"] < filter_capacity:
            continue

        booked_count = len(get_room_bookings(room_name, date_str))
        free_count   = len(TIME_SLOTS) - booked_count
        tag_cls      = TAG_COLORS.get(info["type"], "tag")
        amenity_tags = "".join(f'<span class="tag">{a}</span>' for a in info["amenities"])

        col_card, col_slots = st.columns([1.5, 1])
        with col_card:
            st.markdown(f"""
            <div class="room-card">
                <h3>{room_name}</h3>
                <p class="meta">Floor {info['floor']} &nbsp;&middot;&nbsp; Capacity: {info['capacity']}</p>
                <span class="{tag_cls}">{info['type'].upper()}</span>
                <br>{amenity_tags}
            </div>
            """, unsafe_allow_html=True)
        with col_slots:
            st.markdown(
                f"<div style='padding:0.5rem 0;font-size:0.82rem;color:#9896a0'>"
                f"<b style='color:#f0ebe0'>{date_str}</b> &mdash; "
                f"<span style='color:#50dca0'>{free_count} free</span> / "
                f"<span style='color:#ff6b6b'>{booked_count} booked</span></div>",
                unsafe_allow_html=True,
            )
            for slot in TIME_SLOTS:
                taken_n = slot_seats_taken(room_name, date_str, slot)
                full    = taken_n >= MAX_SEATS
                color   = "#ff6b6b" if full else ("#f0a040" if taken_n > 0 else "#50dca0")
                icon    = "●" if full else ("◑" if taken_n > 0 else "○")
                label   = f"{slot}  ({taken_n}/{MAX_SEATS})"
                st.markdown(
                    f"<div style='font-size:0.79rem;color:{color};line-height:1.85'>{icon} {label}</div>",
                    unsafe_allow_html=True,
                )
        st.markdown("<hr>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    st.markdown("""
    <div class="hero">
        <div class="badge">Info</div>
        <h1>About UniRoom</h1>
        <p>University room reservation system for students.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
**UniRoom** lets students reserve university spaces in seconds — no paperwork, no queues.

#### How it works
1. **Register** with your Student ID, university email and faculty.
2. **Sign in** to your personal account from any device.
3. Go to **Book a Room**, pick a room, date and a free time slot, then confirm.
4. View and cancel reservations anytime under **My Bookings**.
5. Update your name, email or password in **My Profile**.

#### Booking rules
- Slots are **90 minutes** long.
- You can book up to **30 days** in advance.
- Cancel at any time before the slot starts.
- Rooms must be left in the condition they were found in.

#### Time slots
| # | Time |
|---|------|
| 1 | 08:00 – 09:30 |
| 2 | 09:45 – 11:15 |
| 3 | 11:30 – 13:00 |
| 4 | 13:15 – 14:45 |
| 5 | 15:00 – 16:30 |
| 6 | 16:45 – 18:15 |
| 7 | 18:30 – 20:15 |

---
    """)
