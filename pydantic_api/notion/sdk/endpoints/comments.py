from typing import Optional, List

from uuid import UUID

from pydantic_api.notion.models import (
    PageSize,
    StartCursor,
    CreateCommentRequest,
    CreateCommentResponse,
    RetrieveCommentsRequest,
    RetrieveCommentsResponse,
    RichTextObject,
    PageParentObject,
)
from .base import BaseEndpoint


class CommentsEndpoint(BaseEndpoint):
    def create(
        self,
        rich_text: List[RichTextObject],
        parent: Optional[PageParentObject] = None,
        discussion_id: Optional[UUID] = None,
    ):
        """
        Create a comment

        Args:
            rich_text: (List[RichTextObject]) the rich text object, the content of the comment
            parent: (Optional[PageParentObject]) the parent object, either this or a discussion_id is required (not both)
            discussion_id: (Optional[UUID]) the discussion id, either this or a parent object is required (not both)

        Returns:
            CreateCommentResponse: the response object

        Reference:
            https://developers.notion.com/reference/create-a-comment
        """
        raw_req = {
            "rich_text": rich_text,
            "parent": parent,
            "discussion_id": discussion_id,
        }
        validated_req = self._validate_request(
            raw_req=raw_req, pydantic_model=CreateCommentRequest
        )
        raw_resp = self._client.comments.create(**validated_req)
        validated_resp = self._validate_response(
            raw_resp=raw_resp, pydantic_model=CreateCommentResponse
        )
        return validated_resp

    def list(
        self,
        block_or_page_id: UUID,
        start_cursor: Optional[StartCursor] = None,
        page_size: Optional[PageSize] = None,
    ):
        """
        Retrieve comments

        Args:
            block_or_page_id: (UUID) the identifier for a Notion block or page, a uuidv4 string
            start_cursor: (Optional[StartCursor]) If supplied, this endpoint will return a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.
            page_size: (Optional[PageSize]) The number of results to return. The default page size is 100, and the maximum is 100.

        Returns:
            RetrieveCommentsResponse: the response object

        Reference:
            https://developers.notion.com/reference/retrieve-a-comment
        """
        raw_req = {
            "block_id": block_or_page_id,
            "start_cursor": start_cursor,
            "page_size": page_size,
        }
        validated_req = self._validate_request(
            raw_req=raw_req, pydantic_model=RetrieveCommentsRequest
        )
        raw_resp = self._client.comments.list(**validated_req)
        validated_resp = self._validate_response(
            raw_resp=raw_resp, pydantic_model=RetrieveCommentsResponse
        )
        return validated_resp


__all__ = [
    "CommentsEndpoint",
]
