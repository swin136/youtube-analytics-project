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
    my_channel = Channel(get_channels_to_test['MoscowPython'])
    assert my_channel.title == 'MoscowPython'
    assert my_channel.custom_url == 'https://www.youtube.com/@moscowdjangoru'
    # Тестируем получение информации о канале "Мир Православия"
    my_channel = Channel(get_channels_to_test['Мир Православия'])
    assert my_channel.title == 'Мир Православия'
    assert my_channel.custom_url == 'https://www.youtube.com/@user-mirpravoslavia'


def test_access_attribute(get_channels_to_test):
    """Тестируем механизм защиты атрибутов объекта"""
    with pytest.raises(AttributeError):
        my_channel = Channel(get_channels_to_test['MoscowPython'])
        my_channel.channel_id = "Тестовый_канал_id"
