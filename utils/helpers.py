def get_region(server):

    region_map = {
        "na1": "AMERICAS",
        "euw1": "EUROPE",
        "eun1": "EUROPE",
        "kr": "ASIA"
    }

    return region_map.get(server)


def extract_main_player_data(match_data, puuid):

    for p in match_data["info"]["participants"]:

        if p["puuid"] == puuid:
            return p

    raise ValueError("Player not found")