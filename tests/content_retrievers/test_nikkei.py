from datetime import datetime
from zoneinfo import ZoneInfo

from activechat.content_retrievers import Nikkei

UTC = ZoneInfo("UTC")


def test_walk_access_ranking(env):
    """rankingのURL一覧を取得できることを確認する"""
    # Prepare
    nikkei = Nikkei(env)

    # Execute
    actual = nikkei._walk_access_ranking()

    # Assert
    expected_length = 10
    assert len(actual) == expected_length
    assert actual[0] == "https://www.nikkei.com/article/DGXZQOUD061H60W1A201C2000000/"


def test_extract_article(env):
    """記事を取得できることを確認する"""
    # Prepare
    article_url = "https://www.nikkei.com/article/DGXZQOUD061H60W1A201C2000000"

    nikkei = Nikkei(env)

    # Execute
    actual = nikkei._extract_article(article_url)

    # Assert
    assert actual.title == "坂本龍一さん死去、71歳　YMO・「ラストエンペラー」"
    assert actual.content.startswith("映画「ラストエンペラー」で日本人として初めてアカデミー作曲賞を受賞し")  # noqa: E501
    assert actual.source == "nikkei"
    assert actual.article_url == article_url
    assert actual.content_datetime == datetime(2023, 4, 2, 12, 54, 17, 0, UTC)


def test_retrieve_content(env):
    """コンテントを取得できることを確認する"""
    # Prepare
    nikkei = Nikkei(env)

    # Execute
    actual = nikkei.retrieve_content()

    # Assert
    expected_length = 10
    assert len(actual) == expected_length
    assert actual[0].title == "坂本龍一さん死去、71歳　YMO・「ラストエンペラー」"
