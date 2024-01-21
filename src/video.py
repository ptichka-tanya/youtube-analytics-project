import os
import datetime

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео с Youtube"""

    def __init__(self, video_id):
        self.__video_id = video_id
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
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


class PlayList:
    """Класс для плейлиста с Youtube"""

    def __init__(self, playlist_id):
        self.__playlist_id: str = playlist_id
        self.playlist_response: dict = youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.title: str = self.playlist_response['items'][0]['snippet']['title']
        self.url: str = 'https://www.youtube.com/playlist?list=' + self.__playlist_id
        self.playlist_videos: dict = youtube.playlistItems().list(playlistId=playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        self.pl_video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response: dict = youtube.videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.pl_video_ids)
                                                          ).execute()

    def __repr__(self):
        """Отображает информацию об объекте класса в режиме отладки (для разработчиков)"""
        return f'{self.__class__.__name__}({self.__playlist_id})'

    def __str__(self):
        """Отображает информацию об объекте класса для пользователей"""
        return f'{self.title}'

    @property
    def total_duration(self):
        """Взвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста"""

        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        max_num_likes = 0
        max_like_video_id = ''
        for video in self.video_response['items']:
            num_of_likes = int(video['statistics']['likeCount'])
            if num_of_likes > max_num_likes:
                max_like_video_id = video['id']
                max_num_likes = num_of_likes
        return 'https://youtu.be/' + f'{max_like_video_id}'


class PLVideo(PlayList, Video):
    """Класс для видео из определенного плейлиста с Youtube"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        super().__init__(playlist_id)
