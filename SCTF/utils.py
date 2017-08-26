from constance import config
from . import consumers


def game_duration():
    from datetime import timedelta
    return timedelta(
        days=config.GAME_DURATION_DAYS,
        hours=config.GAME_DURATION_HOURS,
        minutes=config.GAME_DURATION_MINS
    )


def set_game_duration(timedelta):
    print(timedelta)
    config.GAME_DURATION_DAYS = timedelta.days
    config.GAME_DURATION_MINS += config.GAME_DURATION_HOURS * 60 - timedelta.seconds / 60
    config.GAME_DURATION_HOURS = 0


def game_end_datetime():
    return config.GAME_START_DATETIME + game_duration()


def send_start_message():
    consumers.send_message(dict(event='GAME_START'))


def send_pause_message():
    consumers.send_message(dict(event='GAME_PAUSE'))


def send_resume_message():
    consumers.send_message(dict(event='GAME_RESUME'))


def send_end_message():
    consumers.send_message(dict(event='GAME_END'))
