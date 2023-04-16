from environs import Env
from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient

from activechat.common.exceptions import SlackSendMessageError, SlackUploadFileError
from activechat.models import Attachment, Reply
from activechat.repliers import Replier


class Slack(Replier):
    """Reply to Slack"""

    def __init__(self, env: Env):
        """init"""
        self.replier = "slack"
        with env.prefixed("SLACK_"):
            self.api_token = env("API_TOKEN")
            self.webhook_url = env("WEBHOOK_URL")

        self.client = WebClient(token=self.api_token)

    def _upload_file(self, attachment: Attachment) -> str:
        try:
            response = self.client.files_upload_v2(
                filename=attachment.filepath.name,
                title=attachment.filepath.name,
                file=str(attachment.filepath.absolute()),
            )
        except SlackApiError as e:
            message = f"failed to upload file: {str(e)}"
            raise SlackUploadFileError(message) from e

        permalink = response["file"]["permalink"]
        return permalink

    def _build_message(self, reply: Reply) -> list[dict]:
        blocks = []
        url_block = {
            "type": "header",
            "text": {"type": "plain_text", "text": reply.title, "emoji": False},
        }
        blocks.append(url_block)
        content_block = {
            "type": "section",
            "text": {"type": "plain_text", "text": reply.content, "emoji": False},
        }
        blocks.append(content_block)
        if reply.url:
            url_block = {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<{reply.url}|view more>"},
            }
            blocks.append(url_block)

        for additional in reply.additionals:
            if isinstance(additional, Attachment):
                permalink = self._upload_file(additional)
                additional_block = {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"<{permalink}|attachment>"},
                }
                blocks.append(additional_block)

        return blocks

    def _post_message(self, blocks: list[dict]):
        try:
            self.client.chat_postMessage(
                channel="#activechat",
                blocks=blocks,
            )
        except SlackApiError as e:
            message = f"failed to send message: {str(e)}"
            raise SlackSendMessageError(message) from e

    def reply_all(self, replies: list[Reply]):
        """Reply using Slack"""
        for reply in replies:
            blocks = self._build_message(reply)
            self._post_message(blocks)
