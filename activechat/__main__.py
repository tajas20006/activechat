from typing import NamedTuple

from environs import Env

from activechat.content_retrievers import ContentRetriever
from activechat.models import Additional, Reply
from activechat.plugins import Plugin
from activechat.repliers import Replier
from activechat.reply_generators import ReplyGenerator


class Pipeline(NamedTuple):
    """pipeline"""

    content_retriever: ContentRetriever
    reply_generator: ReplyGenerator
    plugins: list[Plugin]
    replier: Replier


class ActiveChat:
    """main class for activechat."""

    def __init__(
        self,
        env: Env,
        pipeline: Pipeline,
    ):
        """init."""
        self.envs = env
        self.content_retriever = pipeline.content_retriever
        self.reply_generator = pipeline.reply_generator
        self.plugins = pipeline.plugins
        self.replier = pipeline.replier

    def run(self):
        """run once"""
        contents = self.content_retriever.retrieve_content()
        replies: list[Reply] = []
        for content in contents:
            reply = self.reply_generator.generate_reply(content)
            responses: list[Additional] = []
            for plugin in self.plugins:
                response = plugin.modify_reply_in_place(reply)
                if response:
                    responses.append(response)
            reply.additionals = responses

            replies.append(replies)
        self.replier.reply_all(replies)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    retriever = ContentRetriever.setup(env)
    generator = ReplyGenerator.setup(env)
    plugins = Plugin.setup_all(env)
    replier = Replier.setup(env)
    pipeline = Pipeline(retriever, generator, plugins, replier)

    chat = ActiveChat(env, pipeline)
    chat.run()
