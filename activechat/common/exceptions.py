class AppError(Exception):
    """base exception for activechat application"""


class ConfigError(Exception):
    """there was problem with the config"""


class ZundamonSynthesisError(AppError):
    """Failed to synthesize zundamon voice"""
