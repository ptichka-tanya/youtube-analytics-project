import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется из id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_data = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel_data['items'][0]['snippet']['title']
        self.description = self.channel_data['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subs_count = int(self.channel_data['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel_data['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel_data['items'][0]['statistics']['viewCount'])

    def __repr__(self):
        """Отображает информацию об объекте класса в режиме отладки (для разработчиков)"""
        return f'{self.__class__.__name__}({self.__channel_id})'

    def __str__(self):
        """Отображает информацию об объекте класса для пользователей"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Реализует возможность складывать число подписчиков разных экземпляров класса"""
        return self.subs_count + other.subs_count

    def __sub__(self, other):
        """Реализует возможность вычитать число подписчиков разных экземпляров класса"""
        return self.subs_count - other.subs_count

    def __lt__(self, other):
        """Реализует возможность сравнивать число подписчиков разных экземпляров класса (<)"""
        return self.subs_count < other.subs_count

    def __le__(self, other):
        """Реализует возможность сравнивать число подписчиков разных экземпляров класса (<=)"""
        return self.subs_count <= other.subs_count

    def __gt__(self, other):
        """Реализует возможность сравнивать число подписчиков разных экземпляров класса (>)"""
        return self.subs_count > other.subs_count

    def __ge__(self, other):
        """Реализует возможность сравнивать число подписчиков разных экземпляров класса (>=)"""
        return self.subs_count >= other.subs_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_data))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename: str):
        cannel_attributes = {'channel id': self.__channel_id, 'title': self.title, 'description': self.description,
                             'url': self.url, 'subscriberCount': self.subs_count, 'videoCount': self.video_count,
                             'viewCount': self.view_count}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(cannel_attributes, file, ensure_ascii=False, indent=2)
