from dataclasses import dataclass
import requests
import json
from api_values import API_KEY, PUUID


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
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    DIAMOND = "DIAMOND"
    MASTER = "MASTER"
    ALL = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER"]


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

    def get(self):
        """ Fetch & process a single challenge """
        self.fetch_all_data()
        self.process_single_challenge(self.challenge_name)

    def get_completed(self):
        """ Fetches & processes only completed ARAM challenges and counts them """
        self.fetch_all_data()
        self.completed_count = 0
        self.process_completed_challenges()
        print(f"✅ Completed Challenges: {self.completed_count}")

    def get_uncompleted(self):
        """ Fetches & processes only uncompleted ARAM challenges and counts them """
        self.fetch_all_data()
        self.uncompleted_count = 0
        self.process_uncompleted_challenges()
        print(f"❌ Uncompleted Challenges: {self.uncompleted_count}")

    def fetch_all_data(self):
        """ Fetches challenge configs & user stats in a single API request """
        all_challenges_url = f"https://euw1.api.riotgames.com/lol/challenges/v1/challenges/config?api_key={API_KEY}"
        personal_stats_url = f"https://euw1.api.riotgames.com/lol/challenges/v1/player-data/{PUUID}?api_key={API_KEY}"

        all_challenges_response = requests.get(all_challenges_url)
        personal_stats_response = requests.get(personal_stats_url)

        try:
            self.all_challenges_data = all_challenges_response.json()
            self.personal_stats_data = personal_stats_response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error: API Response is not valid JSON")
            return

    def process_completed_challenges(self):
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
                    self.process_single_challenge(challenge_name)

    def process_uncompleted_challenges(self):
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
                if personal_stats and personal_stats["level"] not in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
                    self.uncompleted_count += 1
                    self.process_single_challenge(challenge_name)

    def process_single_challenge(self, challenge_name):
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
            print(f"📌 Description: {challenge_description}")
            print(f"🏆 Name: {challenge_name}")
            print(f"⭐ Highest Threshold: {highest_tier} - {highest_value}")
            print(f"🎖 Current Level: {current_level}")
            print(f"📊 Current Value: {current_value}")
            print(f"⏳ Missing Until Max Level: {missing_until_max}\n")

    def get_highest_threshold(self, thresholds):
        """ Retrieves the highest challenge tier """
        available_tiers = [tier for tier in ChallengeTiers.ALL if tier in thresholds]
        if available_tiers:
            highest_tier = max(available_tiers, key=lambda tier: ChallengeTiers.ALL.index(tier))
            return {highest_tier: thresholds[highest_tier]}
        return None
