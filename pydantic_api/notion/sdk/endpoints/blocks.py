from typing import Optional, List
from uuid import UUID

from pydantic_api.base import BaseModel
from pydantic_api.notion.models import (
    PageSize,
    StartCursor,
    RetrieveBlockRequest,
    RetrieveBlockResponse,
    RetrieveBlockChildrenRequest,
    RetrieveBlockChildrenResponse,
    DeleteBlockRequest,
    DeleteBlockResponse,
    AppendBlockChildrenRequest,
    AppendBlockChildrenResponse,
    UpdateBlockResponse,
)
from .base import BaseEndpoint


class RetrieveBlockChildrenRequest(BaseModel):
    block_id: UUID
    start_cursor: Optional[StartCursor] = None
    page_size: Optional[PageSize] = None


class BlocksEndpoint(BaseEndpoint):
    def retrieve(
        self,
        block_id: UUID,
    ):
        """
        Retrieve a block.

        Args:
            block_id: (UUID) The identifier of the block.

        Returns:
            RetrieveBlockResponse: The retrieved block object.

        Reference:
            https://developers.notion.com/reference/retrieve-a-block
        """
        raw_req = {"block_id": block_id}
        validated_req = self._validate_request(raw_req, RetrieveBlockRequest)
        raw_resp = self._client.blocks.retrieve(**validated_req)
        return self._validate_response(raw_resp, RetrieveBlockResponse)

    def retrieve_children(
        self,
        block_id: UUID,
        start_cursor: Optional[StartCursor] = None,
        page_size: Optional[PageSize] = None,
    ):
        """
        Retrieve the children of a block.

        Args:
            block_id: (UUID) The identifier of the block.
            start_cursor: (Optional[StartCursor]) The start cursor for pagination.
            page_size: (Optional[PageSize]) The number of results per page.

        Returns:
            RetrieveBlockChildrenResponse: A paginated response containing the block's children.

        Reference:
            https://developers.notion.com/reference/retrieve-block-children
        """
        raw_req = {
            "block_id": block_id,
            "start_cursor": start_cursor,
            "page_size": page_size,
        }
        validated_req = self._validate_request(raw_req, RetrieveBlockChildrenRequest)
        raw_resp = self._client.blocks.children.list(**validated_req)
        return self._validate_response(raw_resp, RetrieveBlockChildrenResponse)

    def append_children(
        self,
        block_id: UUID,
        children: List[dict],
        after: Optional[str] = None,
    ):
        """
        Append children to a block.

        Args:
            block_id: (UUID) The identifier of the block.
            children: (List[dict]) A list of children blocks to append.
            after: (str) The ID of the existing block that the new block should be appended after.

        Returns:
            AppendBlockChildrenResponse: The updated block with the appended children.

        Reference:
            https://developers.notion.com/reference/patch-block-children
        """
        raw_req = {
            "block_id": block_id,
            "children": children,
            "after": after,
        }
        validated_req = self._validate_request(raw_req, AppendBlockChildrenRequest)
        raw_resp = self._client.blocks.children.append(**validated_req)
        return self._validate_response(raw_resp, AppendBlockChildrenResponse)

    def update_block(
        self,
        block_id: UUID,
        properties: dict,
    ):
        """
        Update a block.

        Args:
            block_id: (UUID) The identifier of the block.
            properties: (dict) The properties to update on the block.

        Returns:
            UpdateBlockResponse: The updated block object.

        Reference:
            https://developers.notion.com/reference/update-block
        """
        raw_req = {
            "block_id": block_id,
            **properties,
        }
        raw_resp = self._client.blocks.update(
            **raw_req
        )  # No request validation for update_block
        return self._validate_response(raw_resp, UpdateBlockResponse)

    def delete_block(
        self,
        block_id: UUID,
    ):
        """
        Delete a block.

        Args:
            block_id: (UUID) The identifier of the block.

        Returns:
            DeleteBlockResponse: The deleted block object.

        Reference:
            https://developers.notion.com/reference/delete-a-block
        """
        raw_req = {"block_id": block_id}
        validated_req = self._validate_request(raw_req, DeleteBlockRequest)
        raw_resp = self._client.blocks.delete(**validated_req)
        return self._validate_response(raw_resp, DeleteBlockResponse)


__all__ = [
    "BlocksEndpoint",
]
