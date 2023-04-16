from datetime import datetime
from zoneinfo import ZoneInfo

from environs import Env

from activechat.content_retrievers import ContentRetriever
from activechat.models import Content

JST = ZoneInfo("Asia/Tokyo")


class GoogleNews(ContentRetriever):
    """Retrive contents from Google News."""

    def __init__(self, env: Env):
        """init."""
        self.source = "googlenews"
        with env.prefixed("GOOGLE_NEWS_"):
            self.lang = env.str("LANG")
            self.locale = env.str("LOCALE")

    def retrieve_content(self):
        """Retrive content from Google News."""
        contents = [
            Content(
                title="Title",
                content="Content",
                Source=self.source,
                content_datetime=datetime.now(JST),
            )
        ]
        return contents
