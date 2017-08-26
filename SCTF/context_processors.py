

def config_constant_processor(request):
    from constance import config
    from SCTF.utils import game_end_datetime

    return dict(
        config=config,
        game_end_datetime=game_end_datetime()
    )
