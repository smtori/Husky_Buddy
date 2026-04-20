import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks

st.set_page_config(page_title="Analytical Dashboard", layout="wide")

SideBarLinks()

st.header("Analytical Dashboard")
st.caption("Persona 4: Johanna Park")

if st.button("← Back to Home", type="secondary", use_container_width=False):
    st.switch_page("Home.py")

API_BASES = ["http://api:4000", "http://localhost:4000"]


def fetch_json(path: str):
    last_error = None
    for base in API_BASES:
        try:
            response = requests.get(f"{base}{path}", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
    raise last_error


errors = []

try:
    users_raw = fetch_json("/users")
except Exception as exc:
    users_raw = []
    errors.append(f"Users data unavailable: {exc}")

try:
    matches_raw = fetch_json("/matches")
except Exception as exc:
    matches_raw = []
    errors.append(f"Matches data unavailable: {exc}")

try:
    reports_raw = fetch_json("/reports")
except Exception as exc:
    reports_raw = []
    errors.append(f"Reports data unavailable: {exc}")

for err in errors:
    st.warning(err)

users_df = pd.DataFrame(users_raw)
matches_df = pd.DataFrame(matches_raw)
reports_df = pd.DataFrame(reports_raw)

if not users_df.empty:
    if "status" in users_df.columns:
        users_df["status"] = users_df["status"].fillna("").astype(str).str.lower()
    else:
        users_df["status"] = ""
    if "year" in users_df.columns:
        users_df["year"] = users_df["year"].fillna("Unknown")
    else:
        users_df["year"] = "Unknown"

if not matches_df.empty:
    if "status" in matches_df.columns:
        matches_df["status"] = matches_df["status"].fillna("").astype(str).str.lower()
    else:
        matches_df["status"] = ""
    if "matched_on" in matches_df.columns:
        matches_df["matched_on"] = pd.to_datetime(matches_df["matched_on"], errors="coerce")

if not reports_df.empty:
    if "status" in reports_df.columns:
        reports_df["status"] = reports_df["status"].fillna("").astype(str).str.lower()
    else:
        reports_df["status"] = ""
    if "reason" in reports_df.columns:
        reports_df["reason"] = reports_df["reason"].fillna("Unknown")
    else:
        reports_df["reason"] = "Unknown"

# metrics
total_users = int(len(users_df))
active_matches = int((matches_df["status"] == "active").sum()) if not matches_df.empty else 0
completed_matches = int((matches_df["status"] == "completed").sum()) if not matches_df.empty else 0
removed_matches = int((matches_df["status"] == "removed").sum()) if not matches_df.empty else 0
verified_users = int((users_df["status"] == "verified").sum()) if not users_df.empty else 0

total_non_removed_matches = int((matches_df["status"] != "removed").sum()) if not matches_df.empty else 0
meetup_rate = round((completed_matches / total_non_removed_matches) * 100, 1) if total_non_removed_matches else 0.0
verification_rate = round((verified_users / total_users) * 100, 1) if total_users else 0.0

# top left cards
card1, card2 = st.columns(2)
with card1:
    st.metric("Total Users", total_users)
with card2:
    st.metric("Active Matches", active_matches)

card3, card4 = st.columns(2)
with card3:
    st.metric("Meet Up Rate", f"{meetup_rate:.0f}%")
with card4:
    st.metric("Verification Rate", f"{verification_rate:.0f}%")

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    chart1, chart2 = st.columns(2)

    with chart1:
        with st.container(border=True):
            st.subheader("Sign up Trend")
            if not matches_df.empty and "matched_on" in matches_df.columns:
                trend_df = (
                    matches_df.dropna(subset=["matched_on"])
                    .assign(Month=lambda df: df["matched_on"].dt.strftime("%b"))
                    .groupby("Month", as_index=False)
                    .size()
                    .rename(columns={"size": "Count"})
                )

                month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                trend_df["Month"] = pd.Categorical(trend_df["Month"], categories=month_order, ordered=True)
                trend_df = trend_df.sort_values("Month")

                if len(trend_df) > 0:
                    fig1, ax1 = plt.subplots(figsize=(4, 3))
                    ax1.plot(trend_df["Month"], trend_df["Count"], marker="o", linewidth=2)
                    ax1.spines["top"].set_visible(False)
                    ax1.spines["right"].set_visible(False)
                    ax1.set_xlabel("")
                    ax1.set_ylabel("")
                    ax1.grid(False)
                    st.pyplot(fig1, use_container_width=True)
                else:
                    st.info("No trend data available.")
            else:
                st.info("No trend data available.")

    with chart2:
        with st.container(border=True):
            st.subheader("Demographics")
            if not users_df.empty:
                demo_df = (
                    users_df.groupby("year", as_index=False)
                    .size()
                    .rename(columns={"size": "Users"})
                )

                fig2, ax2 = plt.subplots(figsize=(4, 3))
                ax2.pie(demo_df["Users"], labels=demo_df["year"], autopct="%1.0f%%")
                st.pyplot(fig2, use_container_width=True)
            else:
                st.info("No demographic data available.")

    with st.container(border=True):
        st.subheader("User Satisfaction Survey Results")
        if not reports_df.empty:
            status_counts = (
                reports_df.groupby("status", as_index=False)
                .size()
                .rename(columns={"size": "Count"})
            )
            status_counts["status"] = status_counts["status"].str.title()

            fig3, ax3 = plt.subplots(figsize=(7, 3))
            ax3.barh(status_counts["status"], status_counts["Count"])
            ax3.invert_yaxis()
            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)
            ax3.set_xlabel("")
            ax3.set_ylabel("")
            ax3.grid(False)
            st.pyplot(fig3, use_container_width=True)
        else:
            st.info("No report data available.")

with right_col:
    top1, top2 = st.columns(2)
    with top1:
        st.metric("Successful meet ups", completed_matches)
    with top2:
        st.metric("No meet ups", removed_matches)

    st.metric("In person meetup rate", f"{meetup_rate:.0f}%")

    with st.container(border=True):
        st.subheader("Detailed Breakdown")
        if not matches_df.empty:
            breakdown = (
                matches_df.groupby("status", as_index=False)
                .size()
                .rename(columns={"size": "Total Matches", "status": "Category"})
            )
            breakdown["Category"] = breakdown["Category"].str.title()
            total_matches = max(len(matches_df), 1)
            breakdown["Rate"] = ((breakdown["Total Matches"] / total_matches) * 100).round(0).astype(int)

            for _, row in breakdown.iterrows():
                row_left, row_right = st.columns([3, 2])
                with row_left:
                    st.write(f"**{row['Category']}**")
                    st.caption(f"{row['Total Matches']} total matches")
                with row_right:
                    st.metric("Rate", f"{row['Rate']}%")
                st.divider()
        else:
            st.info("No breakdown data available.")

    with st.container(border=True):
        st.subheader("Common Shared Interests")
        if not reports_df.empty:
            top_reasons = (
                reports_df.groupby("reason", as_index=False)
                .size()
                .rename(columns={"size": "Reports"})
                .sort_values("Reports", ascending=False)
                .head(5)
            )

            for _, row in top_reasons.iterrows():
                r1, r2 = st.columns([3, 1])
                with r1:
                    st.write(f"**{row['reason']}**")
                with r2:
                    st.write(f"{row['Reports']} reports")
                st.divider()
        else:
            st.info("No common issue data available.")
