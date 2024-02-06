"""Tests for api.py"""
import aiohttp
from aioresponses import aioresponses
from ha_wireguard_api.api import WireguardApiClient

from tests import load_fixture


async def test_putting_in_own_session(
    responses: aioresponses,
) -> None:
    """Test putting in own session."""
    responses.get(
        "http://localhost/data.json",
        status=200,
        body=load_fixture("data.json"),
    )
    async with aiohttp.ClientSession() as session:
        client = WireguardApiClient(host="http://localhost/data.json", session=session)
        await client.get_status()
        assert client.session is not None
        await client.close()
        assert client.session is None
