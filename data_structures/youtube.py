"""Common YouTube data structures."""
from datetime import datetime
from typing import List, Optional

from data_structures.base import DataBase


class YouTubeChannel(DataBase):
    # https://developers.google.com/youtube/v3/docs/channels

    def __init__(self,
                 id: str,
                 title: str,
                 created_at: Optional[datetime] = None,
                 description: Optional[str] = None,
                 lang: Optional[str] = None,
                 country: Optional[str] = None):
        super().__init__(
            id=id,
            title=title,
            created_at=created_at,
            description=description,
            lang=lang,
            country=country)

    @property
    def id(self) -> str:
        return self.__getitem__('id')

    @id.setter
    def id(self, value: str):
        self.__setitem__('id', value)

    @property
    def title(self) -> str:
        return self.__getitem__('title')

    @title.setter
    def title(self, value: str):
        self.__setitem__('title', value)

    @property
    def description(self) -> str:
        return self.__getitem__('description')

    @description.setter
    def description(self, value: str):
        self.__setitem__('description', value)

    @property
    def lang(self) -> str:
        return self.__getitem__('lang')

    @lang.setter
    def lang(self, value: str):
        self.__setitem__('lang', value)

    @property
    def country(self) -> str:
        return self.__getitem__('country')

    @country.setter
    def country(self, value: str):
        self.__setitem__('country', value)

    @property
    def created_at(self) -> datetime:
        return self.__getitem__('created_at')

    @created_at.setter
    def created_at(self, value: datetime):
        self.__setitem__('created_at', value)


class YouTubeVideoStats(DataBase):

    def __init__(self,
                 video_id: str,
                 collected_at: datetime,
                 num_views: int,
                 num_likes: int,
                 num_comments: int,
                 num_dislikes: Optional[int] = None):
        super().__init__(
            video_id=video_id,
            collected_at=collected_at,
            num_views=num_views,
            num_likes=num_likes,
            num_comments=num_comments,
            num_dislikes=num_dislikes)

    @property
    def video_id(self) -> str:
        return self.__getitem__('video_id')

    @video_id.setter
    def video_id(self, value: str):
        self.__setitem__('video_id', value)

    @property
    def collected_at(self) -> datetime:
        return self.__getitem__('collected_at')

    @collected_at.setter
    def collected_at(self, value: datetime):
        self.__setitem__('collected_at', value)

    @property
    def num_views(self) -> int:
        return self.__getitem__('num_views')

    @num_views.setter
    def num_views(self, value: int):
        self.__setitem__('num_views', int)

    @property
    def num_likes(self) -> int:
        return self.__getitem__('num_likes')

    @num_likes.setter
    def num_likes(self, value: int):
        self.__setitem__('num_likes', value)

    @property
    def num_comments(self) -> int:
        return self.__getitem__('num_comments')

    @num_comments.setter
    def num_comments(self, value: int):
        self.__setitem__('num_comments', value)

    @property
    def num_dislikes(self) -> int:
        return self.__getitem__('num_dislikes')

    @num_dislikes.setter
    def num_dislikes(self, value: int):
        self.__setitem__('num_dislikes', value)


class YouTubeVideo(DataBase):
    # https://developers.google.com/youtube/v3/docs/videos

    def __init__(self,
                 id : str,
                 channel_id: str,
                 created_at: datetime,
                 title: str,
                 description: str,
                 channel: Optional[YouTubeChannel] = None,
                 stats: Optional[List[YouTubeVideoStats]] = None):
        super().__init__(
            id=id,
            channel_id=channel_id,
            created_at=created_at,
            title=title,
            description=description,
            channel=channel,
            stats=stats)

    @property
    def id(self) -> str:
        return self.__getitem__('id')

    @id.setter
    def id(self, value: str):
        self.__setitem__('id', value)

    @property
    def channel_id(self) -> str:
        return self.__getitem__('channel_id')

    @channel_id.setter
    def channel_id(self, value: str):
        self.__setitem__('channel_id', value)

    @property
    def created_at(self) -> datetime:
        return self.__getitem__('created_at')

    @created_at.setter
    def created_at(self, value: datetime):
        self.__setitem__('created_at', value)

    @property
    def title(self) -> str:
        return self.__getitem__('title')

    @title.setter
    def title(self, value: str):
        self.__setitem__('title', value)

    @property
    def description(self) -> str:
        return self.__getitem__('description')

    @description.setter
    def description(self, value: str):
        self.__setitem__('description', value)

    @property
    def channel(self) -> YouTubeChannel:
        return self.__getitem__('channel')

    @channel.setter
    def channel(self, value: YouTubeChannel):
        self.__setitem__('channel', value)

    @property
    def stats(self) -> YouTubeVideoStats:
        return self.__getitem__('stats')

    @stats.setter
    def stats(self, value: YouTubeVideoStats):
        self.__setitem__('stats', value)


class YouTubeCommentStats(DataBase):

    def __init__(self,
                 comment_id: str,
                 collected_at: datetime,
                 num_likes: int,
                 num_replies: int):
        super().__init__(
            comment_id=comment_id,
            collected_at=collected_at,
            num_likes=num_likes,
            num_replies=num_replies)

    @property
    def comment_id(self) -> str:
        return self.__getitem__('comment_id')

    @comment_id.setter
    def comment_id(self, value: str):
        self.__setitem__('comment_id', value)

    @property
    def collected_at(self) -> datetime:
        return self.__getitem__('collected_at')

    @collected_at.setter
    def collected_at(self, value: datetime):
        self.__setitem__('collected_at', value)

    @property
    def num_likes(self) -> int:
        return self.__getitem__('num_likes')

    @num_likes.setter
    def num_likes(self, value: int):
        self.__setitem__('num_likes', value)

    @property
    def num_replies(self) -> int:
        return self.__getitem__('num_replies')

    @num_replies.setter
    def num_replies(self, value: int):
        self.__setitem__('num_replies', value)


class YouTubeComment(DataBase):
    # https://developers.google.com/youtube/v3/docs/comments

    def __init__(self,
                 id: str,
                 video_id: str,
                 author_channel_id: str,
                 comment_thread_id: str,
                 created_at: datetime,
                 text: str,
                 replied_to_comment_id: Optional[str] = None,
                 channel: Optional[YouTubeChannel] = None,
                 video: Optional[YouTubeVideo] = None,
                 stats: Optional[List[YouTubeCommentStats]] = None):
        super().__init__(
            id=id,
            video_id=video_id,
            author_channel_id=author_channel_id,
            comment_thread_id=comment_thread_id,
            created_at=created_at,
            text=text,
            channel=channel,
            video=video,
            stats=stats,
            replied_to_comment_id=replied_to_comment_id)

    @property
    def id(self) -> str:
        return self.__getitem__('id')

    @id.setter
    def id(self, value: str):
        self.__setitem__('id', value)

    @property
    def video_id(self) -> str:
        return self.__getitem__('video_id')

    @video_id.setter
    def video_id(self, value: str):
        self.__setitem__('video_id', value)

    @property
    def author_channel_id(self) -> str:
        return self.__getitem__('author_channel_id')

    @author_channel_id.setter
    def author_channel_id(self, value: str):
        self.__setitem__('author_channel_id', value)

    @property
    def comment_thread_id(self) -> str:
        return self.__getitem__('comment_thread_id')

    @comment_thread_id.setter
    def comment_thread_id(self, value: str):
        self.__setitem__('comment_thread_id', value)

    @property
    def replied_to_comment_id(self) -> str:
        return self.__getitem__('replied_to_comment_id')

    @replied_to_comment_id.setter
    def replied_to_comment_id(self, value: str):
        self.__setitem__('replied_to_comment_id', value)

    @property
    def created_at(self) -> datetime:
        return self.__getitem__('created_at')

    @created_at.setter
    def created_at(self, value: datetime):
        self.__setitem__('created_at', value)

    @property
    def text(self) -> str:
        return self.__getitem__('text')

    @text.setter
    def text(self, value: str):
        self.__setitem__('text', value)

    @property
    def channel(self) -> YouTubeChannel:
        return self.__getitem__('channel')

    @channel.setter
    def channel(self, value: YouTubeChannel):
        self.__setitem__('channel', value)

    @property
    def video(self) -> YouTubeVideo:
        return self.__getitem__('video')

    @video.setter
    def video(self, value: YouTubeVideo):
        self.__setitem__('video', value)

    @property
    def stats(self) -> List[YouTubeCommentStats]:
        return self.__getitem__('stats')

    @stats.setter
    def stats(self, value: List[YouTubeCommentStats]):
        self.__setitem__('stats', value)
