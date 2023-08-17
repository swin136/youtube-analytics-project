import pytest
from src.channel import Channel
@pytest.fixture()
def get_channels_to_test():
    """Фикстура с тестовыми channel_id каналов YouTube"""
    return {
        'MoscowPython': "UC-OVMPlMA3-YCIeg4z5z23A",
        'Мир Православия': 'UCmSIOnaJ7oLugaqOqI2GnCg',
    }

def test_channel_init(get_channels_to_test):
    """Тестирование инициализации объекта YouTube и получения сведений о канале"""
    # Тестируем получение информации о канале "MoscowPython"
    mychannel = Channel(get_channels_to_test['MoscowPython'])
    assert mychannel.title == 'MoscowPython'
    assert mychannel.custom_url == 'https://www.youtube.com/@moscowdjangoru'
    # Тестируем получение информации о канале "Мир Православия"
    mychannel = Channel(get_channels_to_test['Мир Православия'])
    assert mychannel.title == 'Мир Православия'
    assert mychannel.custom_url == 'https://www.youtube.com/@user-mirpravoslavia'