from environs import Env

from activechat.models import Reply
from activechat.repliers import Replier


class Slack(Replier):
    """Reply to Slack"""

    def __init__(self, env: Env):
        """init"""
        self.replier = "slack"
        with env.prefixed("SLACK_"):
            self.webhook_url = env("WEBHOOK_URL")

    def reply_all(self, replies: list[Reply]):
        """Reply using Slack"""
        pass
