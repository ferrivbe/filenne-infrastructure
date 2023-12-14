from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class PaginatedEntity(BaseModel):
    entities: list[any]
    page: int
    items: int
    next_page: str
    previous_page: str
