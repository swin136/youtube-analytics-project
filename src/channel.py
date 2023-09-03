import json
import os
from pprint import pprint

from dotenv import load_dotenv

from googleapiclient.discovery import build

from src.decorators import check_instance

# Путь к файлу с токеном для доступа к YouTube API
ENV_FILE = '..\\src\\app.env'


class Channel:
    """Класс для ютуб-канала"""
    __youtube_object = None
    __youtube_key = ''

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # Создает объект для доступа к YouTube API
        Channel.__youtube_object = Channel.create_youtube_object()
        # Заполняем атрибуты класса
        # id канала
        self.__channel_id = channel_id.strip()

        channel = Channel.get_service().channels().list(id=self.__channel_id,
                                                        part='snippet,statistics').execute()
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
        self.__viewCount = int(channel.get('items')[0].get('statistics').get('viewCount'))
        # Количество подписчиков
        self.__subscriberCount = (
            int(channel.get('items')[0].get('statistics').get('subscriberCount')))
        # Количество видео на канале
        self.__videoCount = int(channel.get('items')[0].get('statistics').get('videoCount'))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.get_service().channels().list(id=self.__channel_id,
                                                        part='snippet,statistics').execute()
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
                        'video count': self.video_count,
                        }
        file_name_list = [self.title, 'json']
        with open('.'.join(file_name_list), 'w', encoding='utf-8') as file:
            json.dump(channel_dict, file, indent=4)

    def __str__(self):
        """Магический метод для строкового представления объекта класса.
        Шаблон представления <название_канала> (<ссылка_на_канал>)
        """
        return f"{self.title} ({self.url})"

    @check_instance
    def __add__(self, other):
        """Метод суммирует количество подписчиков каналов YouTube"""
        return self.subscriber_count + other.subscriber_count

    @check_instance
    def __sub__(self, other):
        """Метод вычисляет разность количества подписчиков каналов YouTube"""
        return self.subscriber_count - other.subscriber_count

    @check_instance
    def __gt__(self, other):
        """Метод для операции сравнения «больше» для количества подписчиков каналов YouTube"""
        return self.subscriber_count > other.subscriber_count

    @check_instance
    def __ge__(self, other):
        """Метод для операции сравнения «больше или равно» для количества подписчиков
        каналов YouTube"""
        return self.subscriber_count >= other.subscriber_count

    @check_instance
    def __lt__(self, other):
        """Метод для операции сравнения «меньше» для количества подписчиков каналов YouTube"""
        return self.subscriber_count < other.subscriber_count

    @check_instance
    def __le__(self, other):
        """Метод для операции сравнения «меньше или равно» для количества подписчиков
        каналов YouTube"""
        return self.subscriber_count <= other.subscriber_count

    @check_instance
    def __eq__(self, other):
        """Метод для операции сравнения «равно» для количества подписчиков каналов YouTube"""
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        """Возвращает id канала YouTube."""
        return self.__channel_id

    @property
    def title(self):
        """Название канала YouTube."""
        return self.__name

    @property
    def video_count(self):
        """Количество видео на канале YouTube."""
        return self.__videoCount

    @property
    def view_count(self):
        """Общее количество просмотров канала YouTube."""
        return self.__viewCount

    @property
    def subscriber_count(self):
        """Количество подписчиков на канал YouTube."""
        return self.__subscriberCount

    @property
    def url(self):
        """Ссылка на YouTube-канал."""
        return 'https://www.youtube.com/channel/' + self.__channel_id

    @property
    def custom_url(self):
        """Ссылка на YouTube-канал типа @moscowdjangoru."""
        return 'https://www.youtube.com/' + self.__customURL

    @property
    def description(self):
        """Описание канала."""
        return self.__description

    @staticmethod
    def get_service():
        """Возвращает объект для работы с YouTube API."""
        return Channel.__youtube_object

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами."""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    @staticmethod
    def load_credentials():
        """Загрузка токена YouTube из файла в переменную среды."""
        env_file = ENV_FILE
        load_dotenv(env_file)

    @staticmethod
    def create_youtube_object():
        """Создает и возвращает объект для доступа к YouTube API."""
        # Загружаем токен для доступа к YouTube API из env-файла
        Channel.load_credentials()
        api_key: str = os.getenv('YT_KEY')
        # Сохраняем ключ к API в аттрибуте класса
        Channel.__youtube_key = api_key
        # Создаем и возвращаем объект для доступа к Google YouTube API
        return build('youtube', 'v3', developerKey=api_key)

    @staticmethod
    def get_api_key():
        """Возвращает API-ключ, который используется для доступа к сервисам YouTube."""
        return Channel.__youtube_key
