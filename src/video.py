import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Video:
    """Класс для видео с Youtube"""

    def __init__(self, video_id):
        self.__video_id = video_id
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id
                                                         ).execute()
        self.title = self.video_response['items'][0]['snippet']['title']
        self.url = 'https://youtu.be/' + self.__video_id
        self.view_count = int(self.video_response['items'][0]['statistics']['viewCount'])
        self.like_count = int(self.video_response['items'][0]['statistics']['likeCount'])

    def __repr__(self):
        """Отображает информацию об объекте класса в режиме отладки (для разработчиков)"""
        return f'{self.__class__.__name__}({self.__video_id})'

    def __str__(self):
        """Отображает информацию об объекте класса для пользователей"""
        return f'{self.title}'


class PLVideo(Video):
    """Класс для видео из определенного плейлиста с Youtube"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id
