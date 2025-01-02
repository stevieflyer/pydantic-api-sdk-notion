"""
Link Transactions with a Notion Database
"""

from typing import Optional
from abc import ABC, abstractmethod

from uuid import UUID
from pydantic import BaseModel
from pydantic_api.notion.sdk import NotionClient
from pydantic_api.notion.models import (
    Database,
    IconObject,
    CoverObject,
    EmojiObject,
    BlockObject,
    StartCursor,
    PageProperty,
    DatabaseProperty,
    IconObjectFactory,
    NotionPaginatedData,
    ParentObjectFactory,
    RichTextObjectFactory,
)


class NotionDatabaseLinker(ABC):
    def __init__(
        self,
        notion_client: NotionClient,
    ):
        self.notion_client = notion_client
        self.attached_database: Database | None = None
        self.data_model = self.define_data_model()
        self.database_properties = self.define_database_properties()

    # ---- interface ----
    def attach(self, database_name: str, parent_page_id: str | UUID):
        if self.is_attached:
            raise ValueError(
                f"Already attached to a database(id: {self.attached_database_id})."
            )

        existed_databases = self._find_existed_by_name(
            database_name=database_name, parent_page_id=parent_page_id
        )
        existed_database_ids = [db.id for db in existed_databases]
        print(
            f"[attach] found {len(existed_databases)} existed_databases: {existed_database_ids}"
        )
        if len(existed_databases) > 1:
            raise ValueError(
                f"Found {len(existed_databases)}(>1) reserved database with title: {database_name} under root database page(id: {parent_page_id}), ids are: {[db.id for db in existed_databases]}. Please reserve the latest one or just delete them all."
            )
        elif len(existed_databases) == 0:
            self.attached_database = self._create_database(
                database_name=database_name, parent_page_id=parent_page_id
            )
        else:  # len(existed_databases) == 1
            self.attached_database = existed_databases[0]
        return self.attached_database

    def detach(self):
        if self.is_attached:
            self.attached_database = None

    def empty(self):
        """Empty the whole database."""
        if not self.is_attached:
            raise ValueError("Not attached to any database.")
        is_empty = False

        while not is_empty:
            rows = self.notion_client.databases.query(
                database_id=self.attached_database_id
            )
            if len(rows.results) == 0:
                is_empty = True
            print(
                f"[empty notion database {self.attached_database_id}] Found {len(rows.results)} rows. Deleting..."
            )
            for i, row in enumerate(rows.results):
                print(
                    f"[empty notion database {self.attached_database_id}] Deleting {i} / {len(rows.results)} row {row.id}"
                )
                self.notion_client.pages.trash(page_id=row.id)

        print(
            f"[empty notion database {self.attached_database_id}] ✅ Database {self.attached_database_id} is emptied successfully."
        )

    def insert(
        self,
        record: BaseModel,
        icon: IconObject | None = None,
        cover: CoverObject | None = None,
    ):
        if not self.is_attached:
            raise ValueError("Not attached to any database.")
        validated_record = self.data_model.model_validate(record)
        skip_insert = self.not_insert_when(record=validated_record)

        if skip_insert:
            return None

        page = self.notion_client.pages.create(
            icon=icon,
            cover=cover,
            parent=ParentObjectFactory.new_database_parent(
                database_id=self.attached_database_id
            ),
            properties=self._data_to_properties(data=validated_record),
        )

        children = self.__class__.define_page_content(record=validated_record)
        if children:
            self.notion_client.blocks.append_children(
                block_id=str(page.id),
                children=children,
            )

        return page

    # ---- methods to override ----
    def define_emoji_icon(self) -> str | None:
        """Define the emoji icon of the database.

        If not None, you must return a single character emoji icon.

        Example:

        ```python
        def define_emoji_icon(self):
            return "💎"
        ```
        """
        return None

    def define_external_icon(self) -> str | None:
        """Define the external icon of the database.

        If not None, you must return a URL of the external icon.

        Example:

        ```python
        def define_external_icon(self):
            return 'https://www.shutterstock.com/image-illustration/cute-goose-duck-icon-standing-600nw-2441846953.jpg'
        ```
        """
        return None

    def not_insert_when(self, record: BaseModel) -> bool:
        """Define the condition when not to insert the record.

        If the method returns True, the record will not be inserted.

        Example:

        ```python
        def not_insert_when(self, record: BaseModel) -> bool:
            return record.amount < 100
        ```
        """
        return False

    def define_database_properties(self) -> dict[str, DatabaseProperty] | None:
        return None

    @abstractmethod
    def define_data_model(self) -> type[BaseModel]:
        raise NotImplementedError(
            "Please implement the `define_data_model` method to define the data model."
        )

    @classmethod
    def define_page_content(cls, record: BaseModel) -> list[BlockObject]:
        return {}

    @staticmethod
    @abstractmethod
    def _data_to_properties(data: BaseModel) -> dict[str, PageProperty]:
        pass

    # ---- other methods ----
    @property
    def attached_database_id(self):
        return self.attached_database.id if self.attached_database is not None else None

    @property
    def attached_database_title(self):
        return (
            self.attached_database.title if self.attached_database is not None else None
        )

    @property
    def is_attached(self):
        return self.attached_database is not None

    def _validate_emoji_icon(self):
        defined_emoji_icon = self.define_emoji_icon()
        if defined_emoji_icon is not None and len(defined_emoji_icon) != 1:
            raise ValueError(
                f"Emoji icon should be a single character, but got {defined_emoji_icon}."
            )
        return (
            IconObjectFactory.from_emoji(emoji=defined_emoji_icon)
            if defined_emoji_icon
            else None
        )

    def _validate_external_icon(self):
        external_url = self.define_external_icon()
        return (
            IconObjectFactory.from_external_file(url=external_url)
            if external_url
            else None
        )

    def _create_database(self, database_name: str, parent_page_id: str | UUID):
        if self.database_properties is None:
            raise ValueError(
                f"Unsupported action [create_database] for {self.__class__}. Please implement the `define_database_properties` method to support this action."
            )

        icon = self._validate_emoji_icon() or self._validate_external_icon()
        return self.notion_client.databases.create(
            parent=ParentObjectFactory.new_page_parent(
                page_id=parent_page_id,
            ),
            title=[RichTextObjectFactory.new_text(content=database_name)],
            properties=self.database_properties,
            icon=icon,
        )

    def _find_existed_by_name(
        self,
        database_name: str,
        parent_page_id: str | UUID | None,
        start_cursor: Optional[StartCursor] = None,
    ):
        if isinstance(parent_page_id, str):
            parent_page_id = UUID(parent_page_id)

        search_results: NotionPaginatedData[Database] = self.notion_client.search(
            query=database_name,
            filter_value="database",
            start_cursor=start_cursor,
        )

        matched_databases: list[Database] = []
        for database in search_results.results:
            if database.archived:
                continue
            if database.plain_text_title != database_name:
                continue
            if database.parent.type == "page_id" and parent_page_id is not None:
                if parent_page_id != database.parent.page_id:
                    continue
            matched_databases.append(database)

        return matched_databases


__all__ = [
    "NotionDatabaseLinker",
]
