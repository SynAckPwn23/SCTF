

def game_duration():
    from constance import config
    from datetime import timedelta
    return timedelta(
        days=config.GAME_DURATION_DAYS,
        hours=config.GAME_DURATION_HOURS,
        minutes=config.GAME_DURATION_MINS
    )