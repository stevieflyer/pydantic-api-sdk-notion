from typing import Optional, Union
from uuid import UUID
from pydantic import ValidationError

from pydantic_api.notion.models import (
    PageSize,
    StartCursor,
    ListAllUsersRequest,
    ListAllUsersResponse,
    RetrieveUserRequest,
    RetrieveBotUserRequest,
    RetrieveBotUserResponse,
    BotUserObject,
    PersonUserObject,
)
from .base import BaseEndpoint
from ..exception import InvalidRequestError, InvalidResponseError


class UsersEndpoint(BaseEndpoint):
    def list(
        self,
        start_cursor: Optional[StartCursor] = None,
        page_size: Optional[PageSize] = None,
    ):
        """
        List all users

        Args:
            start_cursor: (Optional[StartCursor]) If supplied, this endpoint will return a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.
            page_size: (Optional[PageSize]) The number of results to return. The default page size is 100, and the maximum is 100.

        Returns:
            ListAllUsersResponse: the response object

        Reference:
            https://developers.notion.com/reference/get-users
        """
        raw_req = {
            "start_cursor": start_cursor,
            "page_size": page_size,
        }
        validated_req = self._validate_request(raw_req, ListAllUsersRequest)
        raw_resp = self._client.users.list(**validated_req)
        return self._validate_response(raw_resp, ListAllUsersResponse)

    def retrieve(
        self,
        user_id: UUID,
    ):
        """
        Retrieve a user

        Args:
            user_id: (Union[str, UUID]) the identifier for a Notion user

        Returns:
            BotUserObject | PersonUserObject: the retrieved user object

        Reference:
            https://developers.notion.com/reference/get-user
        """
        raw_req = {"user_id": user_id}
        validated_req = self._validate_request(raw_req, RetrieveUserRequest)
        raw_resp = self._client.users.retrieve(**validated_req)

        try:
            # Special handling for BotUserObject and PersonUserObject
            if "bot" in raw_resp:
                return BotUserObject.model_validate(raw_resp)
            return PersonUserObject.model_validate(raw_resp)
        except ValidationError as e:
            raise InvalidResponseError(raw_response=raw_resp) from e

    def me(self):
        """
        Retrieve your token's bot user

        Args:
            None

        Returns:
            RetrieveBotUserResponse(i.e. BotUserObject): the response object

        Reference:
            https://developers.notion.com/reference/get-self
        """
        raw_req = {}
        validated_req = self._validate_request(raw_req, RetrieveBotUserRequest)
        raw_resp = self._client.users.me(**validated_req)
        return self._validate_response(raw_resp, RetrieveBotUserResponse)


__all__ = [
    "UsersEndpoint",
]
