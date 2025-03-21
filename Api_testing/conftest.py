import pytest

from GD_QA_Portfolio2025.Api_testing.api_client import ApiClient
from config import get_config


@pytest.fixture
def api_client_cats():
    return ApiClient(base_url=get_config()['BASE_URL'])
