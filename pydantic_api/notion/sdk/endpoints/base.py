import json
from abc import ABC
from typing import Any, TypeVar, Type

from notion_client import Client as _Client
from pydantic import BaseModel, ValidationError

from ..exception import InvalidRequestError, InvalidResponseError


T = TypeVar("T", bound=BaseModel)


class BaseEndpoint(ABC):
    def __init__(self, internal_client: _Client):
        self._client = internal_client

    def _validate_request(
        self, raw_req: dict[str, Any], pydantic_model: Type[T]
    ) -> dict[str, Any]:
        try:
            validated_request = pydantic_model.model_validate(raw_req)
        except ValidationError as e:
            raise InvalidRequestError(raw_request=raw_req) from e
        return json.loads(validated_request.model_dump_json(exclude_none=True))

    def _validate_response(self, raw_resp: dict[str, Any], pydantic_model: Type[T]):
        try:
            validated_response = pydantic_model.model_validate(raw_resp)
        except ValidationError as e:
            raise InvalidResponseError(raw_response=raw_resp) from e
        return validated_response


__all__ = [
    "BaseEndpoint",
]
