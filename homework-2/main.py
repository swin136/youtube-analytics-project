from src.channel import Channel

if __name__ == '__main__':
    # Тестовые каналы YouTube
    # MoscowPython
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    # Мир Православия
    # moscowpython = Channel('UCmSIOnaJ7oLugaqOqI2GnCg')

    # получаем значения атрибутов
    print(moscowpython.title)  # MoscowPython
    print(moscowpython.video_count)  # 685 (может уже больше)
    print(moscowpython.url)  # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

    # менять не можем
    try:
        moscowpython.channel_id = 'Новое название'
    except AttributeError:
        print('Ошибка при доступе к атрибуту объекта')
    # AttributeError: property 'channel_id' of 'Channel' object has no setter

    # можем получить объект для работы с API вне класса
    print(Channel.get_service())
    # <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>

    # создаем файл с данными по каналу
    moscowpython.to_json()
