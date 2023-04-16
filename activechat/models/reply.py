from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Additional:
    """Additional"""

    pass


@dataclass
class Attachment(Additional):
    """Audio"""

    filepath: Path


@dataclass
class Reply:
    """Reply"""

    title: str
    content: str
    source: str
    url: str | None = None
    additionals: list[Additional] = field(default_factory=list)
