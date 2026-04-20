import requests
from concurrent.futures import ThreadPoolExecutor


def get_matches(region, puuid, count, api_key):

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}&api_key={api_key}"

    resp = requests.get(url)

    return resp.json()


def get_match_data(region, match_id, api_key):

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"

    return requests.get(url).json()


def get_timeline(region, match_id, api_key):

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}"

    return requests.get(url).json()


def fetch_player_matches(region, puuid, count, api_key):

    matches = get_matches(region, puuid, count, api_key)

    with ThreadPoolExecutor() as executor:

        match_data = list(
            executor.map(lambda m: get_match_data(region, m, api_key), matches)
        )

        timelines = list(
            executor.map(lambda m: get_timeline(region, m, api_key), matches)
        )

    return match_data, timelines