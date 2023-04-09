import hashlib
import json
from pathlib import Path

import requests
from environs import Env
from requests.exceptions import HTTPError, RequestException

from activechat.common.exceptions import ConfigError, ZundamonSynthesisError
from activechat.models import Attachment, Reply
from activechat.plugins import Plugin

SPEAKER_NOT_SET = -1


class Zundamon(Plugin):
    """speak to audio with zundamon."""

    def __init__(self, env: Env):
        """init"""
        with env.prefixed("ZUNDAMON_"):
            self.server = env("SERVER")
            self.character = env("CHARACTER")
            self.style = env("STYLE")

        self.speaker_id = SPEAKER_NOT_SET
        self.tmp_dir: Path = env.path("TMP_DIR", "tmp") / "zundamon"

    def _set_speaker(self):
        try:
            response = requests.get(self.server + "/speakers")
            response.raise_for_status()
        except HTTPError as e:
            message = (
                "failed to get speaker list: "
                f"status_code={response.status_code}, reason={response.text}"
            )
            raise ZundamonSynthesisError(message) from e
        except RequestException as e:
            message = "failed to get speaker list"
            raise ZundamonSynthesisError(message) from e

        for character in response.json():
            if character["name"] != self.character:
                continue
            for style in character["styles"]:
                if style["name"] != self.style:
                    continue
                self.speaker_id = style["id"]
                break
            if self.speaker_id != SPEAKER_NOT_SET:
                break

        if self.speaker_id == SPEAKER_NOT_SET:
            message = (
                "zundamon: specified speaker does not exist: "
                f"character={self.character}, style={self.style}"
            )
            raise ConfigError(message)

    def _generate_key(self, text: str) -> str:
        m = hashlib.sha256()
        m.update(text.encode("utf-8"))
        hashed = m.hexdigest()
        return hashed

    def _audio_query(self, text: str) -> str:
        try:
            response = requests.post(
                self.server + "/audio_query",
                params={"text": text, "speaker": self.speaker_id},
            )
            response.raise_for_status()
        except HTTPError as e:
            message = (
                "failed to create query: "
                f"status_code={response.status_code}, reason={response.text}"
            )
            raise ZundamonSynthesisError(message) from e
        except RequestException as e:
            message = "failed to create query"
            raise ZundamonSynthesisError(message) from e

        query = json.dumps(response.json())
        return query

    def _synthesis(self, query: str) -> bytes:
        try:
            response = requests.post(
                self.server + "/synthesis", params={"speaker": 1}, data=query
            )
            response.raise_for_status()
        except HTTPError as e:
            message = (
                "failed to synthesize: "
                f"status_code={response.status_code}, reason={response.text}"
            )
            raise ZundamonSynthesisError(message) from e
        except RequestException as e:
            message = "failed to synthesize"
            raise ZundamonSynthesisError(message) from e

        content = response.content
        return content

    def _synthesize(self, content: str) -> Path:
        # TODO: split long content into several sections
        key = self._generate_key(content)
        query = self._audio_query(content)
        audio_obj = self._synthesis(query)

        # TODO: concat sections into one file
        # maybe just adding does the job?
        tmp_path = self.tmp_dir / (key + ".wav")
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        with tmp_path.open(mode="wb") as f:
            f.write(audio_obj)
        return tmp_path

    def modify_reply_in_place(self, reply: Reply) -> Attachment:
        """generate audio and add filepath"""
        self._set_speaker()
        filepath = self._synthesize(reply.title + "。" + reply.content)
        audio = Attachment(filepath)
        return audio
