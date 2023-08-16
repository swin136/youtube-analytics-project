import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        Channel.load_credentials()
        api_key: str = os.getenv('YT_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        Channel.printj(channel)

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
    moscowpython.print_info()
