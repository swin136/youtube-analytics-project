import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from pprint import pprint


class Channel:
    """Класс для ютуб-канала"""
    __youtube_object = None

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # Загружаем токен для доступа к YouTube API
        Channel.load_credentials()
        api_key: str = os.getenv('YT_KEY')
        # Создаем объект для доступа к Google YouTube
        self.__youtube = build('youtube', 'v3', developerKey=api_key)
        # Сохраняем ссылку на объект для работы с API вне класса
        Channel.__youtube_object = self.__youtube

        # Заполняем атрибуты класса
        # id канала
        self.__channel_id = channel_id.strip()

        channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # Если вдруг мы не загрузили словарь
        if not isinstance(channel, dict):
            raise TypeError

        # Мы получаем информацию не от канала YouTube
        if channel.get('items')[0].get('kind') != 'youtube#channel':
            raise TypeError

        # название канала
        self.__name = channel.get('items')[0].get('snippet').get('title')
        # описание канала
        self.__description = channel.get('items')[0].get('snippet').get('description')
        # custom URL канала
        self.__customURL = channel.get('items')[0].get('snippet').get('customUrl')
        # Общее количество просмотров
        self.__viewCount = channel.get('items')[0].get('statistics').get('viewCount')
        # Количество подписчиков
        self.__subscriberCount = channel.get('items')[0].get('statistics').get('subscriberCount')
        # Количество видео на канале
        self.__videoCount = channel.get('items')[0].get('statistics').get('videoCount')

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # Channel.printj(channel)
        pprint(channel)

    def to_json(self):
        """Сохраняет в файл значения атрибутов экземпляра Channel.
        Название файла соответствует названию канала YouTube.
        """
        # Создаем словарь
        channel_dict = {'channel name': self.title,
                        'channel_id': self.__channel_id,
                        'description': self.__description,
                        'channel URL': self.url,
                        'channel custom URL': self.custom_url,
                        'subscriber count': self.subscriber_count,
                        'view count': self.view_count,
                        'video count': self.video_count
                        }
        file_name_list = [self.title, 'json']
        with open('.'.join(file_name_list), 'w', encoding='utf-8') as file:
            json.dump(channel_dict, file)

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__name

    @property
    def video_count(self):
        return self.__videoCount

    @property
    def view_count(self):
        return self.__viewCount

    @property
    def subscriber_count(self):
        return self.__subscriberCount

    @property
    def url(self):
        return 'https://www.youtube.com/channel/' + self.__channel_id

    @property
    def custom_url(self):
        return 'https://www.youtube.com/' + self.__customURL

    @property
    def description(self):
        return self.__description

    @staticmethod
    def get_service():
        """Возвращает объект для работы с YouTube API"""
        return Channel.__youtube_object

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    @staticmethod
    def load_credentials():
        """Загрузка токена YouTube в переменную среды"""
        env_file = '..\\src\\app.env'
        load_dotenv(env_file)


if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    # moscowpython = Channel('UCmSIOnaJ7oLugaqOqI2GnCg')
    # moscowpython.print_info()
