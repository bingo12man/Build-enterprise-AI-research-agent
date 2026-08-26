from typing import Optional

from pydantic import BaseModel


class WebSource(BaseModel):
    title: str

    url: str

    content: str

    source_type: str = "web"

    published_date: Optional[str] = None