import httpx
from typing import Optional, Dict, Any, Union, List

from notion_client import Client as _Client
from notion_client.client import ClientOptions

from .endpoints import (
    UsersEndpoint,
    PagesEndpoint,
    BlocksEndpoint,
    SearchEndpoint,
    CommentsEndpoint,
    DatabasesEndpoint,
)


class NotionClient:
    def __init__(
        self,
        options: Optional[Union[Dict[Any, Any], ClientOptions]] = None,
        client: Optional[httpx.Client] = None,
        **kwargs: Any,
    ) -> None:
        self._client = _Client(options=options, client=client, **kwargs)

        # register endpoints
        self.users = UsersEndpoint(self._client)
        self.pages = PagesEndpoint(self._client)
        self.blocks = BlocksEndpoint(self._client)
        self.search = SearchEndpoint(self._client)
        self.comments = CommentsEndpoint(self._client)
        self.databases = DatabasesEndpoint(self._client)


__all__ = [
    "NotionClient",
]
