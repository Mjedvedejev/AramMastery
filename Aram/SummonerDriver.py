from api_values import API_KEY
import requests


def get_RiotID(puuid):
    summoner_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={API_KEY}"
    summoner_url_response = requests.get(summoner_url)
    try:
        summoner_url_data = summoner_url_response.json()
        gameName = summoner_url_data.get("gameName") 
        tagLine = summoner_url_data.get("tagLine")
        return(f"{gameName}#{tagLine}")
    except requests.exceptions.JSONDecodeError:
        return("Error: API Response is not valid JSON")