import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from environs import Env
from slack_sdk.errors import SlackApiError

from activechat.common.exceptions import SlackSendMessageError
from activechat.models import Attachment, Reply
from activechat.repliers import Slack

DATA_DIR = Path() / "tests" / "data"


def test_upload_file(env: Env, attachment: Attachment, client_mock: MagicMock):
    """upload結果からpermalinkを取得できることを確認する"""
    # Prepare
    slack = Slack(env)
    slack.client = client_mock

    # Execute
    actual = slack._upload_file(attachment)

    # Assert
    expected = "http://example.com/d0980ddc49e48475f808e2f270d0445705ffb6f174eff6bdf027f32dfe5660e0.wav"
    assert actual == expected


def test_build_blocks(env: Env, attachment: Attachment, client_mock: MagicMock):
    """slack build kitのブロックを組み立てられることを確認する"""
    # Prepare
    slack = Slack(env)
    slack.client = client_mock

    reply = Reply(
        title="test title",
        content="this is content",
        source="nikkei",
        url="http://example.com",
        additionals=[attachment],
    )

    expect_filepath = DATA_DIR / "slack" / "expected_blocks.json"
    with expect_filepath.open(encoding="utf-8") as f:
        expected = json.load(f)

    # Execute
    actual = slack._build_message(reply)
    assert actual == expected


@pytest.mark.skip("not implemented")
def test_build_blocks__multiple_additionals():
    """複数の付加情報をメッセージに含めることを確認する"""
    raise NotImplementedError


@pytest.mark.skip("not implemented")
def test_build_blocks__no_url():
    """urlがない場合にメッセージを整形できることを確認する"""
    raise NotImplementedError


def test_reply_all(env: Env, attachment: Attachment, client_mock: MagicMock):
    """与えた返信分実行されることを確認する"""
    slack = Slack(env)
    slack.client = client_mock

    replies = [
        Reply(
            title="title1",
            content="content1",
            source="source1",
            url="url1",
            additionals=[attachment],
        ),
        Reply(
            title="title2",
            content="content2",
            source="source2",
        ),
    ]

    slack.reply_all(replies)


def test_reply_all_exception(env: Env, client_mock: MagicMock):
    """slack 送信でエラーがあった場合、例外を投げること"""
    slack = Slack(env)
    slack.client = client_mock
    slack.client.chat_postMessage.side_effect = SlackApiError("", "")

    replies = [Reply(title="title1", content="content1", source="source1")]

    with pytest.raises(SlackSendMessageError):
        slack.reply_all(replies)
