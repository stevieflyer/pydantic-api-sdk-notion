from typing import Optional, Literal, Union

from pydantic_api.notion.models import (
    Page,
    Database,
    SortObject,
    NotionPaginatedData,
    SearchByTitleRequest,
    SearchByTitleFilterObject,
)

from .base import BaseEndpoint


class SearchEndpoint(BaseEndpoint):
    def __call__(
        self,
        query: str,
        sort: Optional[SortObject] = None,
        filter_value: Optional[Literal["database", "page"]] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ):
        """
        Search for pages or databases by title.

        Args:
            query: (str) The text that the API compares page and database titles against.
            sort: (Optional[SortObject]) Sorting criteria, such as direction and timestamp.
            filter_value: (Optional[Literal["database", "page"]]) Filter the search to only include databases or only include pages.
            start_cursor: (Optional[str]) Start cursor for pagination.
            page_size: (Optional[int]) The number of results per page.

        Returns:
            SearchByTitleResponse: A paginated response containing pages or databases.

        Reference:
            https://developers.notion.com/reference/post-search
        """
        raw_req = {
            "query": query,
            "sort": sort,
            "filter": (
                SearchByTitleFilterObject(value=filter_value) if filter_value else None
            ),
            "start_cursor": start_cursor,
            "page_size": page_size,
        }
        validated_req = self._validate_request(raw_req, SearchByTitleRequest)
        raw_resp = self._client.search(**validated_req)
        if filter_value == "database":
            validated_resp = self._validate_response(
                raw_resp, NotionPaginatedData[Database]
            )
        elif filter_value == "page":
            validated_resp = self._validate_response(
                raw_resp, NotionPaginatedData[Page]
            )
        else:
            validated_resp = self._validate_response(
                raw_resp, NotionPaginatedData[Union[Page, Database]]
            )
        return validated_resp


__all__ = [
    "SearchEndpoint",
]
