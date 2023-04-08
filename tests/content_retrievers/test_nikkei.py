from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from environs import Env
from responses import RequestsMock

from activechat.content_retrievers import Nikkei

UTC = ZoneInfo("UTC")

DATA_PATH = Path() / "tests" / "data"


def test_get_html__not_cached(env: Env, mocked_responses: RequestsMock):
    """リクエストを送信することを確認する"""
    # Prepare
    nikkei = Nikkei(env)
    tmp_file = "tmpfile"
    tmp_path = nikkei.tmp_dir / tmp_file
    # キャッシュが存在しない
    tmp_path.unlink(missing_ok=True)
    # リクエストを飛ばすことを確認する
    mocked_responses.get("https://example.com", "test")

    # Execute
    actual = nikkei._get_html("https://example.com", tmp_file)

    # Assert
    assert actual == "test"
    assert tmp_path.exists()


def test_get_html__cached(env: Env):
    """キャッシュから読み込むことを確認する"""
    # Prepare
    nikkei = Nikkei(env)
    tmp_file = "tmpfile"
    tmp_path = nikkei.tmp_dir / tmp_file
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    # キャッシュが存在する
    with tmp_path.open(mode="w", encoding="utf-8") as f:
        f.write("test")

    # Execute
    actual = nikkei._get_html("https://example.com", tmp_file)

    # Assert
    assert actual == "test"


def test_walk_access_ranking(env: Env, mocked_responses: RequestsMock):
    """rankingのURL一覧を取得できることを確認する"""
    # Prepare
    nikkei = Nikkei(env)
    mock_html_path = DATA_PATH / "nikkei" / "ranking_2023040809.html"
    with mock_html_path.open(encoding="utf-8") as f:
        mocked_responses.get(nikkei.url + "/access/", f.read())

    # Execute
    actual = nikkei._walk_access_ranking()

    # Assert
    expected_length = 10
    assert len(actual) == expected_length
    assert actual[0] == "https://www.nikkei.com/article/DGXZQOUE1072E0Q3A210C2000000/"


def test_extract_article(env: Env, mocked_responses: RequestsMock):
    """記事を取得できることを確認する"""
    # Prepare
    article_url = "https://www.nikkei.com/article/DGKKZO70028410Y3A400C2MM0000"
    mock_html_path = DATA_PATH / "nikkei" / "DGKKZO70028410Y3A400C2MM0000.html"
    with mock_html_path.open(encoding="utf-8") as f:
        mocked_responses.get(article_url, f.read())

    nikkei = Nikkei(env)

    # Execute
    actual = nikkei._extract_article(article_url)

    # Assert
    assert actual.title == "テスラ、再び一斉値下げ"
    assert actual.content.startswith("【ニューヨーク=堀田隆文】米電気自動車（EV）大手のテスラが、")  # noqa: E501
    assert actual.source == "nikkei"
    assert actual.article_url == article_url
    assert actual.content_datetime == datetime(2023, 4, 8, 5, 30, 00, 0, UTC)


def test_retrieve_content(env: Env, mocked_responses: RequestsMock):
    """コンテントを取得できることを確認する"""
    # Prepare
    nikkei = Nikkei(env)
    mock_html_path = DATA_PATH / "nikkei" / "ranking_2023040809.html"
    with mock_html_path.open(encoding="utf-8") as f:
        mocked_responses.get(nikkei.url + "/access/", f.read())

    articles = [
        "DGXZQOUE1072E0Q3A210C2000000",
        "DGXZQOUB06DA20W3A400C2000000",
        "DGXZQOFD07DDW0X00C23A4000000",
        "DGXZQOUB093XL0Z00C23A2000000",
        "DGXZQOUD313ZT0R30C23A3000000",
        "DGXZQOUE077SU0X00C23A4000000",
        "DGXZQOCD031XC0T00C23A4000000",
        "DGXZQOUB108TF0Q3A310C2000000",
        "DGXZQOGR07E2E0X00C23A4000000",
        "DGKKZO70028410Y3A400C2MM0000",
    ]
    for article in articles:
        mock_html_path = DATA_PATH / "nikkei" / f"{article}.html"
        mock_url = nikkei.url + "/article/" + article
        with mock_html_path.open(encoding="utf-8") as f:
            mocked_responses.get(mock_url, f.read())

    # Execute
    actual = nikkei.retrieve_content()

    # Assert
    expected_length = 10
    assert len(actual) == expected_length
    assert actual[0].title == "北朝鮮制裁逃れ疑惑の船、日本入港3年で38回　監視に穴"
