from typing import Optional

from pydantic_api.notion.models import SearchByTitleRequest, SearchByTitleResponse

from .base import BaseEndpoint


class SearchEndpoint(BaseEndpoint):
    def __call__(
        self,
        query: str,
        sort: Optional[dict] = None,
        filter: Optional[dict] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ):
        """
        Search for pages or databases by title.

        Args:
            query: (str) The text that the API compares page and database titles against.
            sort: (Optional[dict]) Sorting criteria, such as direction and timestamp.
            filter: (Optional[dict]) Filtering criteria, such as object type.
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
            "filter": filter,
            "start_cursor": start_cursor,
            "page_size": page_size,
        }
        validated_req = self._validate_request(raw_req, SearchByTitleRequest)
        raw_resp = self._client.search(**validated_req)
        return self._validate_response(raw_resp, SearchByTitleResponse)


__all__ = [
    "SearchEndpoint",
]
