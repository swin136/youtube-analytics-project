from src.video import Video, PLVideo


def test_video_class():
    """Проверяем работу экземпляра класса Video"""
    video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
    assert str(video1) == 'GIL в Python: зачем он нужен и как с этим жить'
    assert video1.title == 'GIL в Python: зачем он нужен и как с этим жить'
    assert video1.link_video == 'https://youtu.be/AWX4JnAnjBE'

    video2 = Video('Od6hY_50Dh0')
    assert str(video2) == "Queen - I'm Going Slightly Mad (Official Video)"
    assert video2.link_video == "https://youtu.be/Od6hY_50Dh0"
    assert video2.view_count >= 43_500_000


def test_plvideo_class():
    """Проверяем работу экземпляра класса PLVideo"""
    video = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
    assert str(video) == 'MoscowPython Meetup 78 - вступление'
    assert video.link_video == 'https://youtu.be/4fObz_qw9u4'
    assert video.playlist_id == 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC'


def test_broken_video():
    """Проверяем инициализацию экземпляра класса Video ссылкой на несуществующий видеоролик"""
    broken_video = Video('broken_video_id')
    assert broken_video.title is None
    assert broken_video.like_count is None
