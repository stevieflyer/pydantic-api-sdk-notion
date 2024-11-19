# Type-Safe Notion API SDK

A Python SDK for interacting with the Notion API, featuring **complete IntelliSense support**. Always **up-to-date** with the latest Notion API documentation.

---

## Installation

Install the SDK using pip:

```bash
pip install pydantic-api-sdk-notion
```

## Quick Start

```python
# Import the NotionClient object from the SDK
from pydantic_api.notion.sdk import NotionClient

# Import all Notion-API related types from pydantic_api.notion.models
from pydantic_api.notion.models import (
    TitleDatabaseProperty,
    NumberDatabaseProperty,
    PeopleDatabaseProperty,
    RichTextDatabaseProperty,
    # The SDK provides Factory classes for quick instantiation of Notion API objects
    SortObjectFactory,
    ParentObjectFactory,
    RichTextObjectFactory,
)

# Instantiate a Notion client
notion_api_key = '<your-notion-api-key>'
client = NotionClient(auth=notion_api_key)

# List users
list_user_response = client.users.list(page_size=5)  # Returns `NotionPaginatedData[UserObject]`
print(type(list_user_response.results[0]))  # Prints 'PersonUserObject' or 'BotUserObject'

# Create a new database
new_database = client.databases.create(
    parent=ParentObjectFactory.new_page_parent(
        page_id="13e6c6f3f38d80269039f0186aaf95bb"
    ),
    title=[
        RichTextObjectFactory.new_text(content="🌿 Magical Plant Database"),
    ],
    properties={
        "Plant": TitleDatabaseProperty.define(),
        "Scientific Name": RichTextDatabaseProperty.define(),
        "Price ($)": NumberDatabaseProperty.define(format="dollar"),
        "Discovered By": PeopleDatabaseProperty.define(),
    },
)

# Query the database
records = client.databases.query(
    database_id=new_database.id,
    sorts=[
        SortObjectFactory.new_property_sort(
            property="Price", direction="descending"
        )
    ],
    page_size=3,
)
```

## Additional Notes

The **types used in this SDK** are maintained in a separate GitHub repository:  
[https://github.com/stevieflyer/pydantic-api-models-notion](https://github.com/stevieflyer/pydantic-api-models-notion)

This repository ensures type definitions stay **in sync with the latest Notion API updates**. Developers can directly use these types for their own projects, even without the SDK.
