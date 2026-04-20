from utils.helpers import extract_main_player_data
from utils.performance import calculate_performance_score


def calculate_average_stats(stats):

    total_kills = sum(s["kills"] for s in stats)
    total_deaths = sum(s["deaths"] for s in stats)
    total_assists = sum(s["assists"] for s in stats)

    games = len(stats)

    return {
        "average_kills": round(total_kills / games, 1),
        "average_deaths": round(total_deaths / games, 1),
        "average_assists": round(total_assists / games, 1),
    }


def calculate_and_return_averages(stats_data):

    averages = calculate_average_stats(stats_data)

    cs_rec = averages["average_kills"] < 7
    kda_rec = averages["average_deaths"] < 4

    return averages, cs_rec, kda_rec


def process_data(match_data, timeline_data, puuid, db, player_rank):

    stats = []

    for match in match_data:

        participant = extract_main_player_data(match, puuid)

        stats.append({
            "champion": participant["championName"],
            "kills": participant["kills"],
            "deaths": participant["deaths"],
            "assists": participant["assists"]
        })

    return stats