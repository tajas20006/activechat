from dataclasses import dataclass
from datetime import datetime


@dataclass
class Content:
    """Content."""

    title: str
    content: str
    source: str
    article_url: str
    content_datetime: datetime
