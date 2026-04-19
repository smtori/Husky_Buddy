import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(page_title="User Account Management", layout="wide")

SideBarLinks()

st.header("User Account Management")
if st.button("← Back to Admin Home", type="secondary", use_container_width=False):
    st.switch_page('pages/00_Admin_Home.py')

API_URL = "http://api:4000/users"

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    users = response.json()
except Exception as e:
    st.error(f"Could not load users: {e}")
    users = []

st.caption(f"Loaded {len(users)} users")

search = st.text_input(
    "Search by name or email",
    placeholder="Search by name or email..."
)

if search:
    q = search.lower().strip()
    users = [
        u for u in users
        if q in u["name"].lower() or q in u["email"].lower()
    ]

if "user_filter" not in st.session_state:
    st.session_state["user_filter"] = "All"

if "pending_remove_user" not in st.session_state:
    st.session_state["pending_remove_user"] = None

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("All", key="filter_all", use_container_width=True):
        st.session_state["user_filter"] = "All"
with c2:
    if st.button("Flagged", key="filter_flagged", use_container_width=True):
        st.session_state["user_filter"] = "Flagged"
with c3:
    if st.button("Pending", key="filter_pending", use_container_width=True):
        st.session_state["user_filter"] = "Pending"
with c4:
    if st.button("Suspended", key="filter_suspended", use_container_width=True):
        st.session_state["user_filter"] = "Suspended"

selected_filter = st.session_state["user_filter"]
if selected_filter != "All":
    users = [u for u in users if u["status"].lower() == selected_filter.lower()]

STATUS_ICONS = {
    'pending': '◉',
    'flagged': '⚑',
    'verified': '✓',
    'suspended': '✖'
}

for user in users:
    uid = user["student_id"]
    status = user["status"].lower()
    icon = STATUS_ICONS.get(status, "?")

    with st.container(border=True):
        top_left, top_right = st.columns([5, 2])

        with top_left:
            st.subheader(user["name"])
            st.write(user["email"])
            st.write(user["year"])
            st.write(f"**Student ID:** {uid}")

        with top_right:
            st.metric("Status", f"{icon} {user['status'].title()}")

            if st.session_state["pending_remove_user"] != uid:
                if st.button("Remove user", key=f"remove_user_{uid}", use_container_width=True):
                    st.session_state["pending_remove_user"] = uid
                    st.rerun()
            else:
                st.warning("Are you sure you want to remove this user? This action cannot be undone.")
                c_confirm, c_cancel = st.columns(2)
                with c_confirm:
                    if st.button("Confirm remove", key=f"confirm_remove_{uid}", use_container_width=True):
                        requests.delete(f"http://api:4000/users/{uid}")
                        st.session_state["pending_remove_user"] = None
                        st.rerun()
                with c_cancel:
                    if st.button("Cancel", key=f"cancel_remove_{uid}", use_container_width=True):
                        st.session_state["pending_remove_user"] = None
                        st.rerun()

        st.write("")

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("Flag", key=f"flag_{uid}", use_container_width=True):
                requests.put(f"http://api:4000/users/{uid}", json={**user, "status": "flagged"})
                st.rerun()

        with b2:
            if st.button("Suspend", key=f"suspend_{uid}", use_container_width=True):
                requests.put(f"http://api:4000/users/{uid}", json={**user, "status": "suspended"})
                st.rerun()

        with b3:
            if st.button("Verify", key=f"verify_{uid}", use_container_width=True):
                requests.put(f"http://api:4000/users/{uid}", json={**user, "status": "verified"})
                st.rerun()

    st.write("")