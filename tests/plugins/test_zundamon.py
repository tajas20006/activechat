from environs import Env
from responses import RequestsMock

from activechat.models import Reply
from activechat.plugins import Zundamon


def test_synthesize(env: Env, mocked_responses: RequestsMock):
    """ファイルが出力されることを確認する"""
    zundamon = Zundamon(env)

    mocked_responses.add_passthru(zundamon.server)

    reply = Reply(
        title="自己紹介",
        source="test",
        content="こんにちは、私の名前はずんだもんだもん。",
    )
    actual = zundamon.modify_reply_in_place(reply)

    assert actual.filepath.exists()
