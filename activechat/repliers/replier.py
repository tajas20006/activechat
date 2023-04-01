from abc import ABC, abstractmethod

from environs import Env

from activechat.models import Reply


class Replier(ABC):
    """replier for activechat"""

    @abstractmethod
    def reply_all(self, replies: list[Reply]):
        """reply"""
        raise NotImplementedError

    @classmethod
    def setup(cls, env: Env) -> "Replier":
        """setup"""
        source = env("REPLIER")
        match source:
            case "slack":
                from activechat.repliers import Slack

                return Slack(env)
