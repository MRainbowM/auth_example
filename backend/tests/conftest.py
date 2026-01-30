from config.api import api
from ninja.testing import TestAsyncClient

pytest_plugins = [
    'tests.fixtures'
]

async_client = TestAsyncClient(api)
