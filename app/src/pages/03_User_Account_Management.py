import logging
logger = logging.getLogger(__name__)

import textwrap
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Page config (ONLY once)
st.set_page_config(page_title="User Account Management", layout="wide")

# Sidebar
SideBarLinks()

# Header
st.header("User Account Management")
st.write(f"### Hi, {st.session_state['first_name']}.")

# Styling
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.user-card {
    border: 1.5px solid #222;
    border-radius: 16px;
    padding: 20px 24px 16px 24px;
    margin-bottom: 20px;
    background-color: #f7f7f7;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.user-name {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0;
}

.user-email {
    color: #555;
    font-size: 0.9rem;
    margin: 2px 0;
}

.user-meta {
    color: #777;
    font-size: 0.85rem;
    margin: 2px 0;
}

.status-badge {
    border: 1.5px solid #222;
    border-radius: 20px;
    padding: 6px 16px;
    font-weight: 600;
    font-size: 0.85rem;
    background: white;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.status-verified { border-color: #222; }
.status-pending { border-color: #888; color: #888; }
.status-flagged { border-color: #e07b00; color: #e07b00; }
.status-suspended { border-color: #cc0000; color: #cc0000; }

div.stButton > button {
    border-radius: 14px;
    height: 44px;
    font-weight: 600;
    border: 1.5px solid #222;
    background: white;
}

div.stButton > button:hover {
    background: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# Fetch users from API
try:
    response = requests.get("http://api:4000/users")
    response.raise_for_status()
    users = response.json()
except Exception as e:
    st.error(f"Could not load users: {e}")
    users = []

# Search bar
search = st.text_input(
    "Search",
    label_visibility="collapsed",
    placeholder="Search by name or email..."
)

if search:
    users = [
        u for u in users
        if search.lower() in u["name"].lower()
        or search.lower() in u["email"].lower()
    ]

# Filters
if "user_filter" not in st.session_state:
    st.session_state["user_filter"] = "All"

c1, c2, c3, c4 = st.columns(4)
filters = [("All", c1), ("Flagged", c2), ("Pending", c3), ("Suspended", c4)]

for label, col in filters:
    with col:
        if st.button(label, key=f"filter_{label.lower()}", use_container_width=True):
            st.session_state["user_filter"] = label

selected_filter = st.session_state["user_filter"]

if selected_filter != "All":
    users = [
        u for u in users
        if u["status"].lower() == selected_filter.lower()
    ]

st.write("")

# Icons
STATUS_ICONS = {
    "verified": "✅",
    "pending": "🕐",
    "flagged": "🚩",
    "suspended": "🚫"
}

# Render users
for user in users:
    status = user["status"].lower()
    icon = STATUS_ICONS.get(status, "")
    year = user.get("year", "")
    joined = user.get("joined_date", "")
    joined_row = f"<p class='user-meta'>Joined: {joined}</p>" if joined else ""

    card_html = textwrap.dedent(f"""
    <div class='user-card'>
        <div class='card-header'>
            <div>
                <p class='user-name'>{user['name']}</p>
                <p class='user-email'>{user['email']}</p>
                <p class='user-meta'>{year}</p>
                {joined_row}
            </div>
            <div>
                <span class='status-badge status-{status}'>{icon} {user['status'].title()}</span>
            </div>
        </div>
    </div>
    """)

    st.markdown(card_html, unsafe_allow_html=True)

    uid = user["student_id"]

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        if st.button("🚩 Flag", key=f"flag_{uid}", use_container_width=True):
            requests.put(
                f"http://api:4000/users/{uid}",
                json={**user, "status": "flagged"}
            )
            st.rerun()

    with b2:
        if st.button("🚫 Suspend", key=f"suspend_{uid}", use_container_width=True):
            requests.put(
                f"http://api:4000/users/{uid}",
                json={**user, "status": "suspended"}
            )
            st.rerun()

    with b3:
        if st.button("✅ Verify", key=f"verify_{uid}", use_container_width=True):
            requests.put(
                f"http://api:4000/users/{uid}",
                json={**user, "status": "verified"}
            )
            st.rerun()

    with b4:
        if st.button("🗑 Remove", key=f"delete_{uid}", use_container_width=True):
            requests.delete(f"http://api:4000/users/{uid}")
            st.rerun()

    st.write("")