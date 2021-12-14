from datetime import datetime
from typing import Optional

from data_structures.base import DataBase


class Tweet(DataBase):
    # Tweet model reference
    # v2 api
    # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

    def __init__(self,
                 id: int,
                 text: str,
                 author_id: int,
                 conversation_id: int,
                 created_at: datetime,
                 in_reply_to_user_id: int,
                 lang: str,
                 is_reply: bool,
                 is_retweet: bool,
                 author_name: Optional[str] = None,
                 author_username: Optional[str] = None,
                 author_verified: Optional[bool] = None,
                 author_created_at: Optional[datetime] = None,
                 author_location: Optional[str] = None,
                 author_description: Optional[str] = None,
                 **kwargs):
        super().__init__(
            id=id,
            text=text,
            author_id=author_id,
            conversation_id=conversation_id,
            created_at=created_at,
            in_reply_to_user_id=in_reply_to_user_id,
            lang=lang,
            is_reply=is_reply,
            is_retweet=is_retweet,
            author_name=author_name,
            author_username=author_username,
            author_verified=author_verified,
            author_created_at=author_created_at,
            author_location=author_location,
            author_description=author_description,
            **kwargs)

    @property
    def id(self) -> int:
        return self.__getitem__('id')

    @id.setter
    def id(self, value: int):
        self.__setitem__('id', value)

    @property
    def text(self) -> str:
        return self.__getitem__('text')

    @text.setter
    def text(self, value: str):
        self.__setitem__('text', value)

    @property
    def author_id(self) -> int:
        return self.__getitem__('author_id')

    @author_id.setter
    def author_id(self, value: int):
        self.__setitem__('author_id', value)

    @property
    def conversation_id(self) -> int:
        return self.__getitem__('conversation_id')

    @conversation_id.setter
    def conversation_id(self, value: int):
        self.__setitem__('conversation_id', value)

    @property
    def created_at(self) -> datetime:
        return self.__getitem__('created_at')

    @created_at.setter
    def created_at(self, value: datetime):
        self.__setitem__('created_at', value)

    @property
    def in_reply_to_user_id(self) -> int:
        return self.__getitem__('in_reply_to_user_id')

    @in_reply_to_user_id.setter
    def in_reply_to_user_id(self, value: int):
        self.__setitem__('in_reply_to_user_id', value)

    @property
    def lang(self) -> str:
        return self.__getitem__('lang')

    @lang.setter
    def lang(self, value: str):
        self.__setitem__('lang', value)

    @property
    def is_reply(self) -> bool:
        return self.__getitem__('is_reply')

    @is_reply.setter
    def is_reply(self, value: bool):
        self.__setitem__('is_reply', value)

    @property
    def is_retweet(self) -> bool:
        return self.__getitem__('is_retweet')

    @is_retweet.setter
    def is_retweet(self, value: bool):
        self.__setitem__('is_retweet', value)

    @property
    def author_name(self) -> str:
        return self.__getitem__('author_name')

    @author_name.setter
    def author_name(self, value: str):
        self.__setitem__('author_name', value)

    @property
    def author_username(self) -> str:
        return self.__getitem__('author_username')

    @author_username.setter
    def author_username(self, value: str):
        self.__setitem__('author_username', value)

    @property
    def author_verified(self) -> bool:
        return self.__getitem__('author_verified')

    @author_verified.setter
    def author_verified(self, value: bool):
        self.__setitem__('author_verified', value)

    @property
    def author_created_at(self) -> datetime:
        return self.__getitem__('author_created_at')

    @author_created_at.setter
    def author_created_at(self, value: datetime):
        self.__setitem__('author_created_at', value)

    @property
    def author_location(self) -> str:
        return self.__getitem__('author_location')

    @author_location.setter
    def author_location(self, value: str):
        self.__setitem__('author_location', value)

    @property
    def author_description(self) -> str:
        return self.__getitem__('author_description')

    @author_description.setter
    def author_description(self, value: str):
        self.__setitem__('author_description', value)


class TwitterUser(DataBase):

    def __init__(self,
                 id: int,
                 name: str,
                 username: str,
                 verified: bool,
                 created_at: datetime,
                 location: Optional[str] = None,
                 description: Optional[str] = None,
                 **kwargs):
        super().__init__(
            id=id,
            name=name,
            username=username,
            verified=verified,
            created_at=created_at,
            location=location,
            description=description,
            **kwargs)

    @property
    def id(self) -> int:
        return self.__getitem__('id')

    @id.setter
    def id(self, value: int):
        self.__setitem__('id', value)

    @property
    def name(self) -> str:
        return self.__getitem__('name')

    @name.setter
    def name(self, value: str):
        self.__setitem__('name', value)

    @property
    def username(self) -> str:
        return self.__getitem__('username')

    @username.setter
    def username(self, value: str):
        self.__setitem__('username', value)

    @property
    def verified(self) -> bool:
        return self.__getitem__('verified')

    @verified.setter
    def verified(self, value: bool):
        self.__setitem__('verified', value)

    @property
    def created_at(self) -> datetime:
        return self.__getitem__('created_at')

    @created_at.setter
    def created_at(self, value: datetime):
        self.__setitem__('created_at', value)

    @property
    def location(self) -> str:
        return self.__getitem__('location')

    @location.setter
    def location(self, value: str):
        self.__setitem__('location', value)

    @property
    def description(self) -> str:
        return self.__getitem__('description')

    @description.setter
    def description(self, value: str):
        self.__setitem__('description', value)
