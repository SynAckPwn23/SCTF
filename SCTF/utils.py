from constance import config


def game_duration():
    from datetime import timedelta
    return timedelta(
        days=config.GAME_DURATION_DAYS,
        hours=config.GAME_DURATION_HOURS,
        minutes=config.GAME_DURATION_MINS
    )


def set_game_duration(timedelta):
    config.GAME_DURATION_DAYS = timedelta.days
    config.GAME_DURATION_HOURS = timedelta.hours
    config.GAME_DURATION_MINS = timedelta.minutes


def game_end_datetime():
    return config.GAME_START_DATETIME + game_duration()


def change_game_status(status):
    pass