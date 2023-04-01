from abc import ABC, abstractmethod

from environs import Env

from activechat.models import Content


class ContentRetriever(ABC):
    """content retriever for activechat."""

    @abstractmethod
    def retrieve_content(self) -> list[Content]:
        """retrieve content."""
        raise NotImplementedError

    @classmethod
    def setup(cls, env: Env) -> "ContentRetriever":
        """Create ContentRetriever using configs from env."""
        source = env("CONTENT_RETRIEVER")
        match source:
            case "google-news":
                from activechat.content_retrievers import GoogleNews

                return GoogleNews(env)
