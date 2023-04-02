from environs import Env
from pytest import fixture


@fixture
def env():
    """loads .env"""
    env = Env()
    env.read_env()
    return env
