from zoneinfo import ZoneInfo

from environs import Env

from activechat.models import Content, Reply
from activechat.reply_generators import ReplyGenerator

JST = ZoneInfo("Asia/Tokyo")


class ChatGPT(ReplyGenerator):
    """Generate reply using ChatGPT"""

    def __init__(self, env: Env):
        """init"""
        self.source = "chatgpt"
        with env.prefixed("CHATGPT_"):
            self.lang = env.str("LANG")
            self.locale = env.str("LOCALE")

    def generate_reply(self, content: Content) -> Reply:
        """Generate reply using ChatGPT"""
        reply = Reply(
            title=content.title,
            content=content.content,
            source=content.source,
            additional=[],
        )
        return reply
