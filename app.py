import email
import json
from select import select
import time
from unicodedata import name
import streamlit as st
import requests
import pandas as pd
import datetime as dt
from google.oauth2 import service_account
from gsheetsdb import connect

# set page config
st.set_page_config(page_title="LearnApp", page_icon="favicon.png")

# hide streamlit branding and hamburger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align: center; color: black;'>LA Cohort Leaderboard</h2>",
    unsafe_allow_html=True,
)

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


st.write("----")

cohort_name = st.selectbox("Select the cohort", ["latd-03", "latd-03", "lifs-02"])

sheet_url = st.secrets[f"private_gsheets_url_{cohort_name}"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
# for row in rows:
#     st.write(f"{row.Name} has a score of {round(row.Score)}")

df = pd.DataFrame(rows)[["User_ID", "Name", "Score"]]
df.set_index("User_ID", inplace=True)

st.write("")
st.write("")
st.subheader(f"Leaderboard for {cohort_name.upper()}")
st.dataframe(df)
