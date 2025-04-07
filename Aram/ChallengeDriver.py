from dataclasses import dataclass
import requests
import json
from api_values import API_KEY, PUUID
from SummonerDriver import get_RiotID

@dataclass
class ARAMKeystones:
    ARAMChampion = "ARAM Champion"
    ARAMFinesse = "ARAM Finesse"
    ARAMWarrior = "ARAM Warrior"
    ARAMAuthority = "ARAM Authority"

@dataclass
class ARAMWarrior:
    DPSThreat = "DPS Threat"
    DoubleDecimation = "Double Decimation"
    ARAMLegend = "ARAM Legend"
    BadMedicine = "Bad Medicine"
    NoHiding = "No Hiding"
    ARAMEradication = "ARAM Eradication"
    FarmChampionsNotMinions = "Farm Champions Not Minions"
    SoloCarry = "Solo Carry"

@dataclass
class ARAMFinesse:
    AnotherDayAnotherBullseye = "Another Day, Another Bullseye"
    ItWasANearHit = "It was a... Near-Hit"
    SnowDay = "Snow Day"
    FreeMoney = "Free Money"
    FreeTicketToBase = "Free Ticket to Base"
    PopGoesThePoro = "Pop Goes the Poro"

@dataclass
class ARAMChampion:
    AllRandomAllChampions = "All Random All Champions"
    AllRandomAllFlawless = "All Random All Flawless"
    RapidDemolition = "Rapid Demolition"
    LightningRound = "Lightning Round"
    ActiveParticipant = "Active Participant"
    CantTouchThis = "Can't Touch This"
    NARAM = "NA-RAM"


@dataclass
class ChallengeTiers:
    IRON = "\033[38;5;94mIRON\033[0m"       # Brown-ish
    BRONZE = "\033[38;5;166mBRONZE\033[0m"   # Orange
    SILVER = "\033[38;5;250mSILVER\033[0m"   # Light gray/white
    GOLD = "\033[38;5;220mGOLD\033[0m"       # Yellow/gold
    PLATINUM = "\033[38;5;42mPLATINUM\033[0m" # Green
    DIAMOND = "\033[38;5;33mDIAMOND\033[0m"  # Blue
    MASTER = "\033[38;5;135mMASTER\033[0m"   # Purple
    #GRANDMASTER = "\033[38;5;197mGRANDMASTER\033[0m"  # Crimson Red (used in LoL borders)
    #CHALLENGER = "\033[38;5;226mCHALLENGER\033[0m"    # Bright Gold (like the Challenger crest)
    UNRANKED = "\033[38;5;240mUNRANKED\033[0m"   # Dim gray for unranked



class Challenge:
    PREDEFINED_CHALLENGES = {
        **vars(ARAMKeystones), **vars(ARAMWarrior),
        **vars(ARAMFinesse), **vars(ARAMChampion)
    }

    def __init__(self, challenge_name=None):
        self.challenge_name = challenge_name
        self.all_challenges_data = None
        self.personal_stats_data = None
        self.completed_count = 0
        self.uncompleted_count = 0

    def get(self, puuid):
        """ Fetch & process a single challenge """
        self.fetch_all_data(puuid)
        self.process_single_challenge(self.challenge_name, puuid)

    def get_completed(self, puuid):
        """ Fetches and returns all completed ARAM challenges as structured data """
        self.fetch_all_data(puuid)
        self.completed_count = 0
        results = []

        if not self.all_challenges_data or not self.personal_stats_data:
            print("Error: Data not fetched properly.")
            return results

        for challenge in self.all_challenges_data:
            challenge_name = challenge["localizedNames"]["en_US"]["name"]
            challenge_description = challenge["localizedNames"]["en_US"]["description"]
            challenge_id = challenge["id"]

            if challenge_name in self.PREDEFINED_CHALLENGES.values():
                personal_stats = next(
                    (item for item in self.personal_stats_data["challenges"] if item["challengeId"] == challenge_id),
                    None
                )
                highest_threshold = self.get_highest_threshold(challenge["thresholds"])
                if personal_stats:
                    current_level = personal_stats["level"]
                    current_value = personal_stats["value"]
                    highest_tier = list(highest_threshold.keys())[0] if highest_threshold else None
                    highest_value = list(highest_threshold.values())[0] if highest_threshold else None

                    # Count as completed if current level is MAX or above (Master+)
                    if current_level in ["MASTER", "GRANDMASTER", "CHALLENGER"] or current_level == highest_tier:
                        self.completed_count += 1
                        results.append({
                            "riot_id": get_RiotID(puuid),
                            "name": challenge_name,
                            "description": challenge_description,
                            "current_level": current_level,
                            "current_value": current_value,
                            "highest_level": highest_tier,
                            "highest_value": highest_value,
                            "missing_until_max": 0  # Completed
                        })

        print(f"✅ Completed Challenges: {self.completed_count}")
        return results


    def get_uncompleted(self, puuid):
        """ Fetches and returns all uncompleted ARAM challenges as structured data """
        self.fetch_all_data(puuid)
        self.uncompleted_count = 0
        results = []

        if not self.all_challenges_data or not self.personal_stats_data:
            print("Error: Data not fetched properly.")
            return results

        for challenge in self.all_challenges_data:
            challenge_name = challenge["localizedNames"]["en_US"]["name"]
            challenge_description = challenge["localizedNames"]["en_US"]["description"]
            challenge_id = challenge["id"]

            if challenge_name in self.PREDEFINED_CHALLENGES.values():
                personal_stats = next(
                    (item for item in self.personal_stats_data["challenges"] if item["challengeId"] == challenge_id),
                    None
                )
                highest_threshold = self.get_highest_threshold(challenge["thresholds"])
                if personal_stats:
                    current_level = personal_stats["level"]
                    current_value = personal_stats["value"]
                    highest_tier = list(highest_threshold.keys())[0] if highest_threshold else None
                    highest_value = list(highest_threshold.values())[0] if highest_threshold else None

                    # Only include if not yet completed
                    if highest_tier and (current_level != highest_tier and current_level not in ["GRANDMASTER", "CHALLENGER"]):
                        self.uncompleted_count += 1
                        missing_until_max = highest_value - current_value

                        results.append({
                            "riot_id": get_RiotID(puuid),
                            "name": challenge_name,
                            "description": challenge_description,
                            "current_level": current_level,
                            "current_value": current_value,
                            "highest_level": highest_tier,
                            "highest_value": highest_value,
                            "missing_until_max": missing_until_max
                        })
        print(f"❌ Uncompleted Challenges: {self.uncompleted_count}")
        return results


    def fetch_all_data(self, puuid):
        """ Fetches challenge configs & user stats in a single API request """
        all_challenges_url = f"https://euw1.api.riotgames.com/lol/challenges/v1/challenges/config?api_key={API_KEY}"
        personal_stats_url = f"https://euw1.api.riotgames.com/lol/challenges/v1/player-data/{puuid}?api_key={API_KEY}"

        all_challenges_response = requests.get(all_challenges_url)
        personal_stats_response = requests.get(personal_stats_url)

        try:
            self.all_challenges_data = all_challenges_response.json()
            self.personal_stats_data = personal_stats_response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: API Response is not valid JSON")
            return

    def process_completed_challenges(self, puuid):
        """ Processes and counts all completed ARAM challenges """
        if not self.all_challenges_data or not self.personal_stats_data:
            print("Error: Data not fetched properly.")
            return

        for challenge in self.all_challenges_data:
            challenge_name = challenge["localizedNames"]["en_US"]["name"]
            if challenge_name in self.PREDEFINED_CHALLENGES.values():
                personal_stats = next(
                    (item for item in self.personal_stats_data["challenges"] if item["challengeId"] == challenge["id"]),
                    None
                )
                if personal_stats and personal_stats["level"] in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
                    self.completed_count += 1
                    self.process_single_challenge(challenge_name, puuid)

    def process_uncompleted_challenges(self, puuid):
        """ Processes and counts all uncompleted ARAM challenges """
        if not self.all_challenges_data or not self.personal_stats_data:
            print("Error: Data not fetched properly.")
            return

        for challenge in self.all_challenges_data:
            challenge_name = challenge["localizedNames"]["en_US"]["name"]
            if challenge_name in self.PREDEFINED_CHALLENGES.values():
                personal_stats = next(
                    (item for item in self.personal_stats_data["challenges"] if item["challengeId"] == challenge["id"]),
                    None
                )
                highest_threshold = self.get_highest_threshold(challenge["thresholds"])
                if personal_stats:
                    current_level = personal_stats["level"]
                    highest_tier = list(highest_threshold.keys())[0] if highest_threshold else None

                    # Only count as uncompleted if the current level is BELOW the highest possible tier
                    if highest_tier and (current_level != highest_tier and current_level != "GRANDMASTER" and current_level != "CHALLENGER"):
                        self.uncompleted_count += 1
                        self.process_single_challenge(challenge_name, puuid)

    def process_single_challenge(self, challenge_name, puuid):
        """ Prints challenge info for a single predefined challenge """
        if not self.all_challenges_data or not self.personal_stats_data:
            print("Error: Data not fetched properly.")
            return 

        challenge = next(
            (item for item in self.all_challenges_data if item["localizedNames"]["en_US"]["name"] == challenge_name),
            None
        )

        if not challenge:
            print(f"⚠️ Challenge '{challenge_name}' not found.")
            return

        challenge_description = challenge["localizedNames"]["en_US"]["description"]
        challenge_id = challenge["id"]
        highest_threshold = self.get_highest_threshold(challenge["thresholds"])

        highest_tier = list(highest_threshold.keys())[0]
        highest_value = list(highest_threshold.values())[0]
        # Find the user's stats for this challenge
        personal_stats = next(
            (item for item in self.personal_stats_data["challenges"] if item["challengeId"] == challenge_id),
            None
        )

        if personal_stats:
            current_level = personal_stats["level"]
            current_value = personal_stats["value"]
            missing_until_max = "COMPLETED" if (current_level == highest_tier or current_level in ["GRANDMASTER", "MASTER", "CHALLENGER"]) else highest_value - current_value

            print("\n🔹 Challenge Info:")
            print(f"👊 RiotID: {get_RiotID(puuid)}")
            print(f"📌 Description: {challenge_description}")
            print(f"🏆 Name: {challenge_name}")
            print(f"⭐ Highest Level: {self.get_colored_tier(highest_tier)} - {highest_value}")
            print(f"🎖 Current Level: {self.get_colored_tier(current_level)} - {current_value}")
            print(f"⏳ Missing Until Max Level: {missing_until_max}\n")
    
    def get_challenge_ranking(self):
        if not self.challenge_name:
            print("⚠️ No challenge name specified.")
            return

        rankings = []
        puuid_dict = {k: v for k, v in vars(PUUID).items() if not k.startswith("__")}

        # Fetch challenge config once using any valid puuid
        self.fetch_all_data(next(iter(puuid_dict.values())))

        # Find the challenge ID based on the name
        challenge = next(
            (item for item in self.all_challenges_data if item["localizedNames"]["en_US"]["name"] == self.challenge_name),
            None
        )

        if not challenge:
            print(f"⚠️ Challenge '{self.challenge_name}' not found.")
            return

        challenge_id = challenge["id"]

        for name, puuid in puuid_dict.items():
            url = f"https://euw1.api.riotgames.com/lol/challenges/v1/player-data/{puuid}?api_key={API_KEY}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"⚠️ Failed to fetch data for {name}")
                continue

            try:
                player_data = response.json()
            except requests.exceptions.JSONDecodeError:
                print(f"⚠️ Invalid JSON for {name}")
                continue

            challenge_stats = next(
                (c for c in player_data["challenges"] if c["challengeId"] == challenge_id),
                None
            )

            if challenge_stats:
                value = challenge_stats.get("value", 0)
                level = challenge_stats.get("level", "UNRANKED")
            else:
                value = 0
                level = "UNRANKED"

            rankings.append({
                "Name": name,
                "RiotID": get_RiotID(puuid),
                "Value": value,
                "Level": level
            })

        rankings.sort(key=lambda x: x["Value"], reverse=True)

        print(f"\n📊 Rankings for Challenge: {self.challenge_name}")
        for i, entry in enumerate(rankings, 1):
            print(f"{i}. {entry['RiotID']} ({entry['Name']}) - {self.get_colored_tier(entry['Level'])} - {entry['Value']}")
        return rankings
    
    def get_colored_tier(self, tier: str, html: bool = False) -> str:
        colors = {
            "IRON": "#776e65",
            "BRONZE": "#cd7f32",
            "SILVER": "#c0c0c0",
            "GOLD": "#ffd700",
            "PLATINUM": "#00bfff",
            "DIAMOND": "#b9f2ff",
            "MASTER": "#ff00ff",
            "GRANDMASTER": "#ff3030",
            "CHALLENGER": "#00ffcc"
        }

        if html:
            color = colors.get(tier.upper(), "white")
            return f'<span style="color: {color}; font-weight: bold;">{tier}</span>'
        else:
            return tier  # plain fallback

    def get_highest_threshold(self, thresholds):
        """ Retrieves the highest challenge tier from raw tier names """
        ordered_tiers = list(vars(ChallengeTiers).keys())
        available_tiers = [tier for tier in thresholds.keys() if tier in ordered_tiers]
        if available_tiers:
            highest_tier = max(available_tiers, key=lambda t: ordered_tiers.index(t))
            return {highest_tier: thresholds[highest_tier]}
        return None


