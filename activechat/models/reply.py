from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Additional:
    """Additional"""

    pass


@dataclass
class Audio(Additional):
    """Audio"""

    filepath: Path


@dataclass
class Reply:
    """Reply"""

    title: str
    content: str
    source: str
    additional: list[Additional] = field(default_factory=list)
