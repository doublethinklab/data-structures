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
        self.id = id
        self.title = title
        self.description = description
        self.lang = lang
        self.country = country
        self.created_at = created_at


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
        self.comment_id = comment_id
        self.collected_at = collected_at
        self.num_likes = num_likes
        self.num_replies = num_replies


class YouTubeComment(DataBase):
    # https://developers.google.com/youtube/v3/docs/comments

    def __init__(self,
                 id: str,
                 video_id: str,
                 author_channel_id: str,
                 comment_thread_id: str,
                 created_at: datetime,
                 text: str,
                 stats: List[YouTubeCommentStats],
                 replied_to_comment_id: Optional[str] = None):
        super().__init__(
            id=id,
            video_id=video_id,
            author_channel_id=author_channel_id,
            comment_thread_id=comment_thread_id,
            created_at=created_at,
            text=text,
            stats=stats,
            replied_to_comment_id=replied_to_comment_id)
        self.id = id
        self.video_id = video_id
        self.author_channel_id = author_channel_id
        self.comment_thread_id = comment_thread_id
        self.replied_to_comment_id = replied_to_comment_id
        self.created_at = created_at
        self.text = text  # snippet.textOriginal
        self.stats = stats


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


class YouTubeVideo(DataBase):
    # https://developers.google.com/youtube/v3/docs/videos

    def __init__(self,
                 id : str,
                 channel_id: str,
                 created_at: datetime,
                 title: str,
                 description: str,
                 stats: List[YouTubeVideoStats]):
        super().__init__(
            id=id,
            channel_id=channel_id,
            created_at=created_at,
            title=title,
            description=description,
            stats=stats)
        self.id = id
        self.channel_id = channel_id
        self.created_at = created_at
        self.title = title
        self.description = description
        self.stats = stats
