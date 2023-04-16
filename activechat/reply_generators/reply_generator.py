from abc import ABC, abstractmethod

from environs import Env

from activechat.models import Content, Reply


class ReplyGenerator(ABC):
    """reply generator for activechat"""

    @abstractmethod
    def generate_reply(self, content: Content) -> Reply:
        """generate reply"""
        raise NotImplementedError

    @classmethod
    def setup(cls, env: Env) -> "ReplyGenerator":
        """create ReplyGenerator using config from env"""
        source = env("REPLY_GENERATOR")
        match source:
            case "chatgpt":
                from activechat.reply_generators import ChatGPT

                return ChatGPT(env)
