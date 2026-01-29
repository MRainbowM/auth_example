from config.api import api
from ninja.testing import TestAsyncClient

async_client = TestAsyncClient(api)
