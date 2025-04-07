import streamlit as st
from ChallengeDriver import Challenge, ARAMKeystones, ARAMWarrior, ARAMFinesse, ARAMChampion
from api_values import PUUID
import pandas as pd

st.set_page_config(page_title="ARAM Challenge Tracker", layout="centered")
st.title("🔥 ARAM Challenge Tracker")

# Select user
usernames = [name for name in vars(PUUID) if not name.startswith("__")]
selected_user = st.selectbox("Select Summoner", usernames)
puuid = getattr(PUUID, selected_user)

# Gather all challenge names into a list
def get_all_challenge_names():
    categories = [ARAMKeystones, ARAMWarrior, ARAMFinesse, ARAMChampion]
    names = []
    for cat in categories:
        for k, v in vars(cat).items():
            if not k.startswith("__"):
                names.append(v)
    return sorted(names)

challenge_names = get_all_challenge_names()

# Mode selection
mode = st.radio("What do you want to do?", ["View Single Challenge", "View Completed", "View Uncompleted", "Rank Challenge"])

if mode == "View Single Challenge":
    selected_challenge = st.selectbox("Select a Challenge", challenge_names)
    
    if st.button("Fetch Challenge Info"):
        c = Challenge(selected_challenge)
        c.fetch_all_data(puuid)

        # Grab data from the internal method (rewritten here to extract it)
        challenge = next(
            (item for item in c.all_challenges_data if item["localizedNames"]["en_US"]["name"] == selected_challenge),
            None
        )

        if not challenge:
            st.warning("Challenge not found.")
        else:
            challenge_id = challenge["id"]
            challenge_description = challenge["localizedNames"]["en_US"]["description"]
            highest_threshold = c.get_highest_threshold(challenge["thresholds"])
            highest_tier = list(highest_threshold.keys())[0]
            highest_value = list(highest_threshold.values())[0]

            personal_stats = next(
                (item for item in c.personal_stats_data["challenges"] if item["challengeId"] == challenge_id),
                None
            )

            if personal_stats:
                current_level = personal_stats["level"]
                current_value = personal_stats["value"]
                missing_until_max = (
                    "COMPLETED" if current_level in [highest_tier, "GRANDMASTER", "MASTER", "CHALLENGER"]
                    else highest_value - current_value
                )

                df = pd.DataFrame({
                    "RiotID": [selected_user],
                    "Challenge": [selected_challenge],
                    "Description": [challenge_description],
                    "Current Level": [c.get_colored_tier(current_level, html=True)],
                    "Current Value": [current_value],
                    "Max Level": [c.get_colored_tier(highest_tier, html=True)],
                    "Max Value": [highest_value],
                    "Missing Until Max": [missing_until_max]
                })

                # Render as HTML
                st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.info("No personal stats found for this challenge.")

if mode =="View Completed":
    if st.button("Check Completed"):
        c = Challenge()
        completed = c.get_completed(puuid)
        if completed:
            df = pd.DataFrame([
                {
                    "Challenge Name": item["name"],
                    "Description": item["description"],
                    "Current Level": c.get_colored_tier(item["current_level"], html=True),
                    "Current Value": item["current_value"],
                    "Max Level": c.get_colored_tier(item["highest_level"], html=True),
                    "Max Value": item["highest_value"],
                    "Missing Until Max": item["missing_until_max"]
                }
                for item in completed
            ])
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No completed challenges found.")


elif mode == "View Uncompleted":
    if st.button("Check Uncompleted"):
        c = Challenge()
        uncompleted = c.get_uncompleted(puuid)

        if uncompleted:
            # Assuming uncompleted is a list of dictionaries like:
            # [{'name': 'ARAM Authority', 'description': '...', 'current_level': 'DIAMOND', ...}, ...]

            # Format it into a DataFrame
            df = pd.DataFrame([
                {
                    "Challenge Name": item.get("name"),
                    "Description": item.get("description"),
                    "Current Level": c.get_colored_tier(item.get("current_level", ""), html=True),
                    "Current Value": item.get("current_value"),
                    "Max Level": c.get_colored_tier(item.get("highest_level", ""), html=True),
                    "Max Value": item.get("highest_value"),
                    "Missing Until Max": item.get("missing_until_max")
                }
                for item in uncompleted
            ])

            # Show the table with HTML formatting for tier colors
            st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("No uncompleted challenges found.")



elif mode == "Rank Challenge":
    selected_challenge = st.selectbox("Select a Challenge to Rank", challenge_names)
    if st.button("Get Rankings"):
        c = Challenge(selected_challenge)
        rankings = c.get_challenge_ranking()

        if rankings:
            df = pd.DataFrame(rankings)
            df["Level"] = df["Level"].apply(lambda tier: c.get_colored_tier(tier))
            st.dataframe(df)
