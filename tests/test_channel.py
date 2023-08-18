import pytest
from src.channel import Channel


@pytest.fixture
def get_channels_to_test():
    """Фикстура с тестовыми channel_id каналов YouTube"""
    return {
        'MoscowPython': Channel("UC-OVMPlMA3-YCIeg4z5z23A"),
        'Мир Православия': Channel('UCmSIOnaJ7oLugaqOqI2GnCg'),
    }


def test_channel_init(get_channels_to_test):
    """Тестирование инициализации объекта YouTube и получения сведений о канале"""
    # Тестируем получение информации о канале "MoscowPython"
    my_channel = get_channels_to_test['MoscowPython']
    assert my_channel.title == 'MoscowPython'
    assert my_channel.custom_url == 'https://www.youtube.com/@moscowdjangoru'
    # Тестируем получение информации о канале "Мир Православия"
    my_channel = get_channels_to_test['Мир Православия']
    assert my_channel.title == 'Мир Православия'
    assert my_channel.custom_url == 'https://www.youtube.com/@user-mirpravoslavia'


def test_access_attribute(get_channels_to_test):
    """Тестируем механизм защиты атрибутов объекта"""
    with pytest.raises(AttributeError):
        my_channel = get_channels_to_test['MoscowPython']
        my_channel.channel_id = "Тестовый_канал_id"


def test_repr_method(get_channels_to_test):
    """Тестируем метод строкового представления объекта класса"""
    my_channel = get_channels_to_test['MoscowPython']
    assert str(my_channel) == 'MoscowPython (https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A)'

    my_channel = get_channels_to_test['Мир Православия']
    assert str(my_channel) == 'Мир Православия (https://www.youtube.com/channel/UCmSIOnaJ7oLugaqOqI2GnCg)'


def test_add_method(get_channels_to_test):
    """Тестируем магический метод __add__ для сложения подписчиков каналов YouTube"""
    channel_1 = get_channels_to_test['MoscowPython']
    channel_2 = get_channels_to_test['Мир Православия']
    result_sum = channel_1.subscriber_count + channel_2.subscriber_count

    assert channel_1 + channel_2 == result_sum


def test_sub_method(get_channels_to_test):
    """Тестируем магический метод __sub__ для разности подписчиков каналов YouTube"""
    channel_1 = get_channels_to_test['MoscowPython']
    channel_2 = get_channels_to_test['Мир Православия']
    result_sub = channel_1.subscriber_count - channel_2.subscriber_count

    assert channel_1 - channel_2 == result_sub


def test_check_instance(get_channels_to_test):
    """Тестируем работу декоратора, проверяющего соответствие типов экземпляров классов, над которыми проводятся
    арифметические и логические операции"""
    # Корректный канал
    channel_legal = get_channels_to_test['MoscowPython']

    # Создаем произвольный класс, у экземпляра которого будет аттрибут subscriber_count
    class IllegalChannel:
        def __init__(self, subscriber_count):
            self.subscriber_count = subscriber_count

    # Инициализируем экземпляр "неправильного" класса для тестов
    channel_illegal = IllegalChannel(126760)

    # Тестируем операцию сложения
    result_sum = channel_legal.subscriber_count + channel_illegal.subscriber_count
    with pytest.raises(TypeError):
        assert channel_legal + channel_illegal == result_sum

    # Тестируем операцию вычитания
    result_sub = channel_legal.subscriber_count - channel_illegal.subscriber_count
    with pytest.raises(TypeError):
        assert channel_legal - channel_illegal == result_sub

    # Тесты для логических операций
    # операция равнения "равно"
    # Выравниваем значение аттрибутов subscriber_count у экземпляров классов IllegalChannel и Channel
    channel_illegal.subscriber_count = channel_legal.subscriber_count
    with pytest.raises(TypeError):
        assert channel_legal == channel_illegal
