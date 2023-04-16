import json
from pathlib import Path
from unittest.mock import MagicMock

from pytest import fixture
from pytest_mock import MockerFixture
from slack_sdk.web import WebClient

from activechat.models import Attachment


@fixture
def attachment(data_dir: Path) -> Attachment:
    """return attachment"""
    filepath = (
        data_dir
        / "slack"
        / "d0980ddc49e48475f808e2f270d0445705ffb6f174eff6bdf027f32dfe5660e0.wav"
    )
    a = Attachment(filepath)
    return a


@fixture
def client_mock(mocker: MockerFixture, data_dir: Path) -> MagicMock:
    """return mocked slack client"""
    client_mock = mocker.MagicMock(spec_set=WebClient)
    response_mock = data_dir / "slack" / "upload_file_response.json"
    with response_mock.open(encoding="utf-8") as f:
        client_mock.files_upload_v2.return_value = json.load(f)
    return client_mock
