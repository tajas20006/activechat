from pathlib import Path

import pytest
from environs import Env
from responses import RequestsMock

from activechat.common.exceptions import ConfigError
from activechat.models import Reply
from activechat.plugins import Zundamon
from tests.testutils import ci

DATA_PATH = Path() / "tests" / "data"

SPEAKER_NOT_SET = -1


@pytest.mark.parametrize(
    ("in_character", "in_style", "out_speaker_id"),
    [
        ("ずんだもん", "ノーマル", 3),
        ("四国めたん", "ツンツン", 6),
        ("ずんだもん", "no_such_style", SPEAKER_NOT_SET),
        ("no_such_character", "ノーマル", SPEAKER_NOT_SET),
    ],
    ids=["normal_zundamon", "tsuntsun_metan", "no_such_style", "no_such_character"],
)
def test_set_speaker(
    env: Env, mocked_responses: RequestsMock, in_character, in_style, out_speaker_id
):
    """設定値に従ったスピーカーが選ばれることを確認する"""
    # Prepare
    zundamon = Zundamon(env)
    zundamon.character = in_character
    zundamon.style = in_style

    mock_speakers = DATA_PATH / "zundamon" / "speakers.json"
    with mock_speakers.open(encoding="utf-8") as f:
        mocked_responses.get(zundamon.server + "/speakers", f.read())

    # Execute
    if out_speaker_id == SPEAKER_NOT_SET:
        with pytest.raises(ConfigError):
            zundamon._set_speaker()
    else:
        zundamon._set_speaker()

    # Assert
    assert zundamon.speaker_id == out_speaker_id


@ci
def test_synthesize(env: Env, mocked_responses: RequestsMock):
    """ファイルが出力されることを確認する"""
    # Prepare
    zundamon = Zundamon(env)

    mocked_responses.add_passthru(zundamon.server)

    reply = Reply(
        title="自己紹介",
        source="test",
        content="こんにちは、私の名前はずんだもんだもん。",
    )

    # Execute
    actual = zundamon.modify_reply_in_place(reply)

    # Assert
    assert actual.filepath.exists()
