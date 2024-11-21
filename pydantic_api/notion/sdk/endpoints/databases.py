from typing import Optional, List, Dict

from uuid import UUID
from pydantic_api.notion.models import (
    CreateDatabaseRequest,
    CreateDatabaseResponse,
    QueryDatabaseRequest,
    QueryDatabaseResponse,
    RetrieveDatabaseRequest,
    RetrieveDatabaseResponse,
    UpdateDatabaseRequest,
    UpdateDatabaseResponse,
    DatabaseProperty,
    RichTextObject,
    PageParentObject,
    FilterObject,
    SortObject,
    StartCursor,
    PageSize,
    IconObject,
    CoverObject,
)
from .base import BaseEndpoint


class DatabasesEndpoint(BaseEndpoint):
    def create(
        self,
        parent: PageParentObject,
        title: List[RichTextObject],
        properties: Dict[str, DatabaseProperty],
        icon: Optional[IconObject] = None,
        cover: Optional[CoverObject] = None,
    ):
        """
        Create a new database.

        Args:
            parent: (PageParentObject) The parent page where the database is created.
            title: (List[RichTextObject]) The title of the database as it appears in Notion.
            properties: (Dict[str, DatabaseProperty) The property schema of the database.
            icon: (Optional[IconObject]) The icon of the database. Not listed in the documentation but shown in the official example.
            cover: (Optional[CoverObject]) The cover of the database. Not listed in the documentation but shown in the official example.

        Returns:
            CreateDatabaseResponse: The created database object.

        Reference:
            https://developers.notion.com/reference/create-a-database
        """
        raw_req = {
            "parent": parent,
            "title": title,
            "properties": properties,
            "cover": cover,
            "icon": icon,
        }
        validated_req = self._validate_request(raw_req, CreateDatabaseRequest)
        raw_resp = self._client.databases.create(**validated_req)
        return self._validate_response(raw_resp, CreateDatabaseResponse)

    def query(
        self,
        database_id: UUID,
        filter: Optional[FilterObject] = None,
        sorts: Optional[List[SortObject]] = None,
        start_cursor: Optional[StartCursor] = None,
        page_size: Optional[PageSize] = None,
    ):
        """
        Query a database.

        Args:
            database_id: (UUID) The identifier for the database.
            filter: (Optional[FilterObject]) Filtering conditions.
            sorts: (Optional[List[SortObject]]) Sorting criteria.
            start_cursor: (Optional[StartCursor]) Start cursor for pagination.
            page_size: (Optional[PageSize]) The number of results per page.

        Returns:
            QueryDatabaseResponse: A paginated response containing pages or databases.

        Reference:
            https://developers.notion.com/reference/post-database-query
        """
        raw_req = {
            "database_id": database_id,
            "filter": filter,
            "sorts": sorts,
            "start_cursor": start_cursor,
            "page_size": page_size,
        }
        validated_req = self._validate_request(raw_req, QueryDatabaseRequest)
        raw_resp = self._client.databases.query(**validated_req)
        return self._validate_response(raw_resp, QueryDatabaseResponse)

    def retrieve(self, database_id: UUID):
        """
        Retrieve a database.

        Args:
            database_id: (UUID) The identifier for the database.

        Returns:
            RetrieveDatabaseResponse: The retrieved database object.

        Reference:
            https://developers.notion.com/reference/retrieve-a-database
        """
        raw_req = {"database_id": database_id}
        validated_req = self._validate_request(raw_req, RetrieveDatabaseRequest)
        raw_resp = self._client.databases.retrieve(**validated_req)
        return self._validate_response(raw_resp, RetrieveDatabaseResponse)

    def update(
        self,
        database_id: UUID,
        title: Optional[List[RichTextObject]] = None,
        description: Optional[List[RichTextObject]] = None,
        properties: Optional[Dict[str, DatabaseProperty]] = None,
    ):
        """
        Update a database.

        Args:
            database_id: (UUID) The identifier for the database.
            title: (Optional[List[RichTextObject]]) New title for the database.
            description: (Optional[List[RichTextObject]]) New description for the database.
            properties: (Optional[Dict[str, DatabaseProperty]]) Properties to be updated or added.

        Returns:
            UpdateDatabaseResponse: The updated database object.

        Reference:
            https://developers.notion.com/reference/update-a-database
        """
        raw_req = {
            "database_id": database_id,
            "title": title,
            "description": description,
            "properties": properties,
        }
        validated_req = self._validate_request(raw_req, UpdateDatabaseRequest)
        raw_resp = self._client.databases.update(**validated_req)
        return self._validate_response(raw_resp, UpdateDatabaseResponse)


__all__ = [
    "DatabasesEndpoint",
]
