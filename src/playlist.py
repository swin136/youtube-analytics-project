import datetime

import isodate

import requests

from src.channel import Channel
from src.video import Video


class PlayList:
    """Класс для работы с плейлистом YouTube"""
    __youtube_object = None

    def __init__(self, playlist_id: str):
        # Создает объект для доступа к YouTube API
        if PlayList.__youtube_object is None:
            PlayList.__youtube_object = Channel.create_youtube_object()

        playlist_title = PlayList.get_playlist_title(Channel.get_api_key(), playlist_id)
        if playlist_title is None:
            self.__title = None
        self.__title = playlist_title
        self.__playlist_id = playlist_id

    @staticmethod
    def get_playlist_title(api_key: str, playlist_id: str):
        """Метод для получения названия плейлиста YouTube по id"""
        # Готовим url и заголовки для запроса к API
        url = (f'https://www.googleapis.com/youtube/v3/playlists?key={api_key}&id'
               f'={playlist_id}&part=id,snippet&fields=items(id,snippet(title,channelId,'
               'channelTitle))')
        headers = {
            "Accept": "*/*",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 "
                "Safari/537.36",
        }
        # Отправляем запрос с сервису
        response = requests.get(url, headers)
        # Обрабатываем ответ, извлекаем из словаря наименование плейлиста,
        # который и возвращаем (в случае ошибки возвращаем None)
        if response.status_code == 200:
            try:
                data = response.json()
                return data['items'][0]['snippet']['title']
            except (requests.exceptions.JSONDecodeError, IndexError, KeyError):
                return

    @property
    def total_duration(self):
        """возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста"""
        playlist_videos = (
            PlayList.__youtube_object.playlistItems().list(playlistId=self.__playlist_id,
                                                           part='contentDetails',
                                                           maxResults=50).execute())

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId']
                                for video in playlist_videos['items']]
        # вывести длительности видеороликов из плейлиста
        video_response = PlayList.__youtube_object.videos().list(part='contentDetails,statistics',
                                                                 id=','.join(video_ids)).execute()
        # Инициализируем счетчик общей длительности видеороликов в плейлисте
        total_duration = datetime.timedelta(hours=0, minutes=0, seconds=0)
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        # Получаем все видео в плейлисте
        playlist_videos = PlayList.__youtube_object.playlistItems().list(
            playlistId=self.__playlist_id, part='contentDetails', maxResults=50).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId']
                                for video in playlist_videos['items']]
        # Ищем видео с наибольшим числом лайков
        favorite_link = str(None)
        search_like = 0
        for sample_video in video_ids:
            video = Video(sample_video)
            if video.like_count > search_like:
                favorite_link = video.link_video
                search_like = video.like_count

        return favorite_link

    @property
    def title(self):
        """Возвращает наименование плейлиста"""
        return self.__title

    @property
    def url(self):
        """Возвращает ссылку на плейлист"""
        if self.__title is None:
            return
        return f'https://www.youtube.com/playlist?list={self.__playlist_id}'
