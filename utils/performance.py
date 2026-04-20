def calculate_performance_score(
    kills,
    assists,
    cs_per_min,
    vision_score,
    dragon_kills,
    weights
):

    normalized_cs = cs_per_min / 8

    score = (
        kills * weights["kills"]
        + assists * weights["assists"]
        + normalized_cs * weights["cs_per_min"]
        + vision_score * weights["visionScore"]
        + dragon_kills * weights["dragonKills"]
    )

    return round(score, 2)