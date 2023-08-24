import datetime
from src.playlist import PlayList


def test_playlist():
    """Проверяем работу экземпляра класса PlayList"""
    pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
    assert pl.title == "Moscow Python Meetup №81"
    assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"

    duration = pl.total_duration
    assert str(duration) == "1:49:52"
    assert isinstance(duration, datetime.timedelta)
    assert duration.total_seconds() == 6592.0

    assert pl.show_best_video() == "https://youtu.be/cUGyMzWQcGM"


def test_broken_video():
    """Проверяем инициализацию экземпляра класса Playlist ссылкой на несуществующий плейлист YouTube"""
    broken_playlist = PlayList('broken_playlist_id')
    assert broken_playlist.title is None
    assert broken_playlist.url is None
