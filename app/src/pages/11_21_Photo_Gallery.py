import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks
import time

st.set_page_config(layout='wide')

SideBarLinks()

BASE_URL = "http://web-api:4000"


current_user_id = st.session_state.get('user_id', 1)
first_name = str(st.session_state.get('first_name', '')).strip().lower()
return_page = st.session_state.get('match_chat_return_page')

if not return_page:
    if first_name == 'natalie':
        return_page = 'pages/20_Natalie_Home.py'
    elif first_name == 'brandon':
        return_page = 'pages/10_Brandon_Home.py'
    elif current_user_id == 2:
        return_page = 'pages/20_Natalie_Home.py'
    else:
        return_page = 'pages/10_Brandon_Home.py'

if st.button("← Back to Options", type="secondary", use_container_width=False):
    st.switch_page(return_page)
st.header(f"My HuskyBuddy Photo Gallery")
st.write(f"### Hi, {st.session_state['first_name']}.")

# ── Load Photos ─────────────────────────────────────────────
def load_photos():
    try:
        resp = requests.get(f"{BASE_URL}/users/{current_user_id}/photos")
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error("Could not load photos.")
            return []
    except requests.exceptions.RequestException:
        st.error("Could not connect to the API.")
        return []

photos = load_photos()

if not photos:
    st.info("No meetup photos yet! Complete a HuskyBuddy chat and upload a photo to get started.")
else:
    st.write(f"### You have {len(photos)} meetup photo(s)!")
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        with cols[i % 3]:
            st.image(
                photo["photo_url"],
                use_container_width=True
            )
            st.caption(f"📍 {photo['caption']}")
            st.write(f"Uploaded by **{photo['first_name']} {photo['last_name']}**")
            st.write(f"🗓️ {photo['uploaded_at'][:16]}")
            st.divider()

# ── Upload New Photo ────────────────────────────────────────
st.write("---")
st.subheader("Upload a New Photo")

# Display success message if upload just completed
if st.session_state.get('photo_upload_success'):
    st.success("Photo uploaded successfully!")
    st.session_state['photo_upload_success'] = False
    time.sleep(2)
    st.rerun()

# Load user's matches for dropdown
def load_user_matches():
    try:
        resp = requests.get(f"{BASE_URL}/matches?student_id={current_user_id}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def get_user_name(user_id):
    try:
        resp = requests.get(f"{BASE_URL}/users/{user_id}")
        if resp.status_code == 200:
            data = resp.json()
            return f"{data.get('first_name', '')} {data.get('last_name', '')}"
        else:
            return f"User {user_id}"
    except requests.exceptions.RequestException:
        return f"User {user_id}"

matches_list = load_user_matches()

if not matches_list:
    st.info("No matches available. Complete a HuskyBuddy match first to upload photos.")
else:
    with st.form("upload_photo_form"):
        # Create match options for dropdown with buddy names
        match_options = {}
        for match in matches_list:
            match_id = match['match_id']
            status = match['status']
            # Determine which user is the buddy and get their name
            buddy_id = match['student2_id'] if match['student1_id'] == current_user_id else match['student1_id']
            buddy_name = get_user_name(buddy_id)
            
            display_name = f"{buddy_name} ({status})"
            match_options[display_name] = match_id
        
        if match_options:
            selected_match = st.selectbox("Select Match", options=list(match_options.keys()))
            match_id = match_options[selected_match]
        else:
            st.warning("Could not load match details.")
            match_id = None
        
        caption = st.text_area("Caption")
        photo_url = st.text_input("Photo URL")
        submitted = st.form_submit_button("Upload Photo")

        if submitted:
            if not caption:
                st.error("Caption is required.")
            elif not photo_url:
                st.error("Please provide a photo URL.")
            elif not match_id:
                st.error("Please select a match.")
            else:
                try:
                    resp = requests.post(
                        f"{BASE_URL}/users/{current_user_id}/photos",
                        json={
                            "match_id": match_id,
                            "photo_url": photo_url,
                            "caption": caption
                        }
                    )
                    if resp.status_code == 201:
                        st.session_state['photo_upload_success'] = True
                        st.rerun()
                    else:
                        st.error(f"Failed to upload: {resp.json().get('error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the API: {str(e)}")