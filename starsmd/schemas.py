from typing import Optional

from pydantic import BaseModel, field_validator


class Repository(BaseModel):
    name: str
    html_url: str
    description: Optional[str] = ""
    topics: Optional[list[str]] = []

    @field_validator("topics")
    def append_hash_tag(cls, topics):
        return [f"#{topic}" for topic in topics]
