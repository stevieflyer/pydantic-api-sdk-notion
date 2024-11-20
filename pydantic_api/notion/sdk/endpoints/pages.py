from typing import Optional, Union, Dict, List

from uuid import UUID

from pydantic_api.notion.models import (
    CreatePageRequest,
    CreatePageResponse,
    RetrievePageRequest,
    RetrievePageResponse,
    RetrievePagePropertyItemRequest,
    RetrievePagePropertyItemResponse,
    UpdatePagePropertiesRequest,
    UpdatePagePropertiesResponse,
    PageParentObject,
    DatabaseParentObject,
    IconObject,
    CoverObject,
    PageProperty,
)
from .base import BaseEndpoint


class PagesEndpoint(BaseEndpoint):
    def create(
        self,
        parent: Union[PageParentObject, DatabaseParentObject],
        properties: Dict[str, PageProperty],
        children: Optional[List] = None,
        icon: Optional[IconObject] = None,
        cover: Optional[CoverObject] = None,
    ):
        """
        Create a page in a database or as a subpage.

        Args:
            parent: The parent page or database where the new page is inserted.
            properties: The values of the page's properties.
            children: The content to be rendered on the new page.
            icon: The icon of the new page.
            cover: The cover image of the new page.

        Returns:
            CreatePageResponse: the created page object.

        Reference:
            https://developers.notion.com/reference/post-page
        """
        raw_req = {
            "parent": parent,
            "properties": properties,
            "children": children or [],
            "icon": icon,
            "cover": cover,
        }
        validated_req = self._validate_request(raw_req, CreatePageRequest)
        raw_resp = self._client.pages.create(**validated_req)
        return self._validate_response(raw_resp, CreatePageResponse)

    def retrieve(self, page_id: UUID, filter_properties: Optional[list[str]] = None):
        """
        Retrieve a Notion page.

        Args:
            page_id: The identifier for the page.
            filter_properties: A list of page property value IDs to filter.

        Returns:
            RetrievePageResponse: the retrieved page object.

        Reference:
            https://developers.notion.com/reference/retrieve-a-page
        """
        raw_req = {"page_id": page_id, "filter_properties": filter_properties}
        validated_req = self._validate_request(raw_req, RetrievePageRequest)
        raw_resp = self._client.pages.retrieve(**validated_req)
        return self._validate_response(raw_resp, RetrievePageResponse)

    # def retrieve_property_item(
    #     self,
    #     page_id: UUID,
    #     property_id: str,
    #     start_cursor: Optional[str] = None,
    #     page_size: Optional[int] = None,
    # ):
    #     """
    #     Retrieve a property item from a Notion page.

    #     Args:
    #         page_id: The identifier for the page.
    #         property_id: The identifier for the property.
    #         start_cursor: The cursor for pagination.
    #         page_size: The number of results per page.

    #     Returns:
    #         RetrievePagePropertyItemResponse: the retrieved property object.

    #     Reference:
    #         https://developers.notion.com/reference/retrieve-a-page-property
    #     """
    #     raw_req = {
    #         "page_id": page_id,
    #         "property_id": property_id,
    #         "start_cursor": start_cursor,
    #         "page_size": page_size,
    #     }
    #     validated_req = self._validate_request(raw_req, RetrievePagePropertyItemRequest)
    #     raw_resp = self._client.pages.retrieve_property(**validated_req)
    #     return self._validate_response(raw_resp, RetrievePagePropertyItemResponse)

    def update_properties(
        self,
        page_id: UUID,
        properties: Optional[Dict[str, PageProperty]] = None,
        archived: Optional[bool] = None,
        icon: Optional[IconObject] = None,
        cover: Optional[CoverObject] = None,
    ):
        """
        Update the properties of a Notion page.

        Args:
            page_id: The identifier for the page to update.
            properties: The property values to update.
            archived: Whether to archive or unarchive the page.
            icon: A page icon for the page.
            cover: A cover image for the page.

        Returns:
            UpdatePagePropertiesResponse: the updated page object.

        Reference:
            https://developers.notion.com/reference/patch-page
        """
        raw_req = {
            "page_id": page_id,
            "properties": properties,
            "archived": archived,
            "icon": icon,
            "cover": cover,
        }
        validated_req = self._validate_request(raw_req, UpdatePagePropertiesRequest)
        raw_resp = self._client.pages.update(**validated_req)
        return self._validate_response(raw_resp, UpdatePagePropertiesResponse)


__all__ = [
    "PagesEndpoint",
]
