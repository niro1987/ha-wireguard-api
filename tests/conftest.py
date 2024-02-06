"""
This is a configuration file for pytest containing customizations and fixtures.
"""
from collections.abc import AsyncGenerator, Generator

import aiohttp
from aioresponses import aioresponses
import pytest

from ha_wireguard_api.api import WireguardApiClient


@pytest.fixture(name="wireguard_api_client")
async def client() -> AsyncGenerator[WireguardApiClient, None]:
    """Return a Spotify client."""
    async with aiohttp.ClientSession() as session, WireguardApiClient(
        host="http://localhost",
        session=session,
    ) as wireguard_api_client:
        yield wireguard_api_client


@pytest.fixture(name="responses")
def aioresponses_fixture() -> Generator[aioresponses, None, None]:
    """Return aioresponses fixture."""
    with aioresponses() as mocked_responses:
        yield mocked_responses
