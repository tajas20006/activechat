from environs import Env

from activechat.models import Audio, Reply
from activechat.plugins import Plugin


class Zundamon(Plugin):
    """speak to audio with zundamon."""

    def __init__(self, env: Env):
        """init"""
        with env.prefixed("ZUNDAMON_"):
            self.character = env("CHARACTER")
            self.type = env("TYPE")

    def modify_reply_in_place(self, reply: Reply) -> Reply:
        """generate audio and add filepath"""
        filepath = "audio.wav"
        audio = Audio(filepath)
        reply.additional.append(audio)
