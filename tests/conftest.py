import shutil

import responses
from environs import Env
from pytest import fixture
from pytest_mock import MockerFixture


@fixture(autouse=True)
def mocked_responses():
    """globally activate responses"""
    with responses.RequestsMock() as rsps:
        yield rsps


@fixture(autouse=True)
def delete_tmp_dir(env: Env):
    """delete tmp dir after each test"""
    yield
    tmp_dir = env.path("TMP_DIR", "tmp")
    shutil.rmtree(tmp_dir, ignore_errors=True)


@fixture(autouse=True)
def env(mocker: MockerFixture):
    """mock environ and load .env"""
    mocker.patch.dict("os.environ", {}, clear=True)
    env = Env()
    env.read_env("tests/.env.example")
    yield env
