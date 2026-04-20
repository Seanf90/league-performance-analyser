import requests


def get_player_info(summoner_name, server, api_key):

    url = f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"

    headers = {"X-Riot-Token": api_key}

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return None, None

    data = resp.json()

    return data["puuid"], data["id"]


def get_rank(server, encrypted_id, api_key):

    url = f"https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_id}"

    headers = {"X-Riot-Token": api_key}

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        return None, None

    data = resp.json()

    for entry in data:

        if entry["queueType"] == "RANKED_SOLO_5x5":

            rank = entry["tier"] + " " + entry["rank"]
            lp = entry["leaguePoints"]

            return rank, lp

    return None, None


def fetch_player_info(name, server, api_key):

    puuid, encrypted_id = get_player_info(name, server, api_key)

    if not puuid:
        return None, None, None, None

    rank, lp = get_rank(server, encrypted_id, api_key)

    if not rank:
        rank = "Unranked"
        lp = ""

    return puuid, encrypted_id, rank, lp