from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup
from environs import Env

from activechat.content_retrievers import ContentRetriever
from activechat.models import Content

UTC = ZoneInfo("UTC")


class Nikkei(ContentRetriever):
    """Retrieve contents from Nikkei access ranking"""

    def __init__(self, env: Env):
        """init"""
        self.source = "nikkei"
        self.url = "https://www.nikkei.com"
        self.tmp_dir: Path = env.path("TMP_DIR", "tmp") / "nikkei"

    def _get_html(self, url: str, tmp_file: str) -> str:
        tmp_path = self.tmp_dir / tmp_file
        if tmp_path.exists():
            with tmp_path.open(encoding="utf-8") as f:
                html_content = f.read()
        else:
            response = requests.get(url)
            html_content = response.text
            tmp_path.parent.mkdir(parents=True, exist_ok=True)
            with tmp_path.open(mode="w", encoding="utf-8") as f:
                f.write(html_content)
        return html_content

    def _walk_access_ranking(self) -> list[str]:
        url = self.url + "/access/"
        now = datetime.now(UTC)
        tmp_file = f"ranking_{now.strftime('%Y%m%d%H')}.html"
        html_content = self._get_html(url, tmp_file)

        soup = BeautifulSoup(html_content, "html.parser")

        ranking = soup.find("ul", class_="m-miM32_list")
        article_urls = [self.url + a["href"] for a in ranking.find_all("a")]
        return article_urls

    def _extract_article(self, article_url: str) -> Content:
        article_url = article_url.rstrip("/")
        tmp_file = f"{article_url.split('/')[-1]}.html"
        html_content = self._get_html(article_url, tmp_file)

        soup = BeautifulSoup(html_content, "html.parser")

        title = soup.find("h1").text
        content = "\n".join(
            [p.text for p in soup.find_all("p", class_="paragraph_p15tm1hb")]
        )
        content_datetime = datetime.fromisoformat(soup.find("time")["datetime"])

        content = Content(
            title=title,
            content=content,
            source=self.source,
            article_url=article_url,
            content_datetime=content_datetime,
        )
        return content

    def retrieve_content(self):
        """Retrieve content from nikkei"""
        article_urls = self._walk_access_ranking()

        contents: list[Content] = []
        for article_url in article_urls:
            content = self._extract_article(article_url)
            contents.append(content)

        return contents
