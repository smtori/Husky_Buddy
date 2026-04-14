import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('User Account Management')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

st.set_page_config(page_title="User Account Management", layout="wide")
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.user-card {
    border: 1px solid #222;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: #f7f7f7;
}

.status-badge {
    border: 1px solid #222;
    border-radius: 12px;
    padding: 12px 20px;
    text-align: center;
    font-weight: 600;
    background: white;
    margin-top: 20px;
}

div.stButton > button {
    border-radius: 14px;
    height: 48px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Mock user data for the time being
users = [
    {
        "name": "Brandon Heller",
        "email": "heller.b@northeastern.edu",
        "major": "Business",
        "joined": "2026-02-12",
        "status": "Verified"
    },
    {
        "name": "Natalie Frost",
        "email": "frost.n@northeastern.edu",
        "major": "Business",
        "joined": "2025-10-19",
        "status": "Pending"
    }
]

st.title("User Account Management")
st.write(f"### Hi, {st.session_state['first_name']}.")

search = st.text_input(
    "Search by name or email...",
    label_visibility="collapsed",
    placeholder="Search by name or email..."
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.button("All", key="filter_all", use_container_width=True)
with c2:
    st.button("Flagged", key="filter_flagged", use_container_width=True)
with c3:
    st.button("Pending", key="filter_pending", use_container_width=True)
with c4:
    st.button("Suspended", key="filter_suspended", use_container_width=True)

st.write("")

for user in users:
    st.markdown("<div class='user-card'>", unsafe_allow_html=True)

    info_col, status_col = st.columns([4, 2])

    with info_col:
        st.markdown(f"### {user['name']}")
        st.markdown(user["email"])
        st.markdown(user["major"])
        st.markdown(f"**Joined:** {user['joined']}")

    with status_col:
        st.markdown(
            f"<div class='status-badge'>{user['status']}</div>",
            unsafe_allow_html=True
        )

    b1, b2, b3 = st.columns(3)
    with b1:
        st.button("Flag", key=f"flag_{user['email']}", use_container_width=True)
    with b2:
        st.button("Suspend", key=f"suspend_{user['email']}", use_container_width=True)
    with b3:
        st.button("Verify", key=f"verify_{user['email']}", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)