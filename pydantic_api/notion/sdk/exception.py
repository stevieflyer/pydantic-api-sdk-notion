from typing import Union
from pydantic import BaseModel


class InvalidRequestError(Exception):
    def __init__(self, raw_request: Union[dict, BaseModel]):
        # Convert the raw_request to a dictionary if it's a BaseModel instance
        if isinstance(raw_request, BaseModel):
            raw_request = raw_request.model_dump()

        # Construct the error message
        error_message = f"Invalid Request: {raw_request}"

        # Call the base class constructor with the error message
        super().__init__(error_message)

        # Store the request data for further debugging if needed
        self.raw_request = raw_request


class InvalidResponseError(Exception):
    def __init__(self, raw_response: dict):
        # Construct the error message
        error_message = f"Invalid Response: {raw_response}"

        # Call the base class constructor with the error message
        super().__init__(error_message)

        # Store the response data for further debugging if needed
        self.raw_response = raw_response


__all__ = [
    "InvalidRequestError",
    "InvalidResponseError",
]
