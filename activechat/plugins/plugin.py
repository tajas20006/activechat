from abc import ABC, abstractmethod

from environs import Env

from activechat.models import Reply


class Plugin(ABC):
    """Plugin to modify reply"""

    @abstractmethod
    def modify_reply_in_place(self, reply: Reply):
        """modify reply.

        mainly used to add additional to reply.
        """
        raise NotImplementedError

    @classmethod
    def setup_all(cls, env: Env) -> list["Plugin"]:
        """setup plugins"""
        plugins = []

        plugin_names = env.list("PLUGINS")
        for plugin_name in plugin_names:
            match plugin_name:
                case "zundamon":
                    from activechat.plugins import Zundamon

                    plugin = Zundamon(env)
                    plugins.append(plugin)

        return plugin
