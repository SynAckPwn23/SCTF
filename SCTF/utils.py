
from constance import config
from . import consumers


def game_duration():
    from datetime import timedelta
    return timedelta(
        days=config.GAME_DURATION_DAYS,
        hours=config.GAME_DURATION_HOURS,
        minutes=config.GAME_DURATION_MINS
    )

def set_game_duration(delta):
    from datetime import timedelta
    duration = timedelta(
        days=config.GAME_DURATION_DAYS,
        seconds=config.GAME_DURATION_HOURS * 3600 + config.GAME_DURATION_MINS * 60
    )
    new_duration = duration - delta
    config.GAME_DURATION_DAYS = new_duration.days
    config.GAME_DURATION_HOURS = 0
    config.GAME_DURATION_MINS = new_duration.seconds / 60


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
