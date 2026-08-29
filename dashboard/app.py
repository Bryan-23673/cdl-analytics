import streamlit as st
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

CITO_API_KEY = os.getenv("CITO_API_KEY")

# Name of the app
st.title("Call of Duty League Analysis")

with st.container():
    # WINNER OF THE TOURNMANET IS THE FIRST THING PEOPLE SHOULD SEE

    # GET REQUEST for CDL 2026 CHAMPIONSHIP 2026 matches
    cdl_matches_url = "https://api.citoapi.com/api/v1/cod/tournaments/codwiki-call-of-duty-league-championship-2026/matches"
    headers = {
        "x-api-key" : CITO_API_KEY
    }

    get_request_cdl_matches = requests.get(cdl_matches_url, headers=headers)
    cdl_matches_json = get_request_cdl_matches.json()

    # Make a dataframe to hold data
    matches_df = pd.json_normalize(cdl_matches_json["data"])

    # clean the data and organize
    matches_df[(matches_df["tournament.tournamentId"] == "cdl-2026-championship") & (matches_df["status"] == "completed")] .copy()
    matches_df["matchDate"] = pd.to_datetime(matches_df["matchDate"])
    matches_df = matches_df.sort_values("matchDate", ascending=False)

    # Get the tournament name, the most recent round, winner, and winner logo
    most_recent_match = matches_df.iloc[0]

    round = most_recent_match["round"]
    tournament_name = most_recent_match["tournament.name"]
    team1 = most_recent_match["team1.name"]
    team2 = most_recent_match["team2.name"]

    # Find which team won and get their logo
    if int(most_recent_match["team1.score"]) > int(most_recent_match["team2.score"]):
        winner = team1
        winner_logo_url = most_recent_match["team1.logoUrl"]
    else:
        winner = team2
        winner_logo_url = most_recent_match["team2.logoUrl"]

    st.header(f"Winner of the {tournament_name} Tournament")
    st.image(winner_logo_url, caption=f"{tournament_name} Winner - {winner}", width=500)

    # Second thing people should see are the players of the team with their stats of the entire tournamenet
    players = ""
