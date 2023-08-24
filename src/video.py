from src.channel import Channel
from pprint import pprint


class Video:
    """Класс для ролика YouTube"""
    __youtube_obj = None
    def __init__(self, video_id: str) -> None:
        # Создает объект для доступа к YouTube API
        if Video.__youtube_obj is None:
            Video.__youtube_obj = Channel.create_youtube_object()
        # Заполняем аттрибуты экземпляра класса
        self.__video_id = video_id

        video_response = Video.__youtube_obj.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=self.video_id
                                                              ).execute()

        try:
            # название видео
            self.__title = video_response['items'][0]['snippet']['title']

            # количество просмотров
            self.__viewCount = int(video_response['items'][0]['statistics']['viewCount'])
            # количество лайков
            self.__likeCount = int(video_response['items'][0]['statistics']['likeCount'])
        except (IndexError, KeyError):
            self.__title = None
            self.__viewCount = None
            self.__likeCount = None

    def print_video_info(self):
        video_response = Video.__youtube_obj.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=self.video_id).execute()
        pprint(video_response)

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return (f"название видео: {self.title}\n"
                f"id video: {self.__video_id}\n"
                f"ссылка на видео: {self.link_video}\n"
                f"количество просмотров: {self.view_count}\n"
                f"количество лайков: {self.like_count}")

    @property
    def video_id(self):
        return self.__video_id

    @property
    def youtube_object(self):
        return Video.__youtube_obj

    @property
    def title(self):
        return self.__title

    @property
    def view_count(self):
        return self.__viewCount

    @property
    def like_count(self):
        return self.__likeCount

    @property
    def link_video(self):
        # return f'https://www.youtube.com/watch?v={self.video_id}'
        return f'https://youtu.be/{self.video_id}'


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    def __repr__(self):
        return super().__repr__() + '\n' + f"id плейлиста: {self.playlist_id}"
