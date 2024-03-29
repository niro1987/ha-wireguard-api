"""Asynchronous client for WireGuard status API."""
import asyncio
from dataclasses import dataclass
from typing import Any, Self

from aiohttp import ClientSession

from .const import REQUEST_TIMEOUT, REQUIRED_STATUS
from .exceptions import WireGuardResponseError, WireGuardTimeoutError
from .model import WireGuardPeer


@dataclass
class WireguardApiClient:
    """Asynchronous client for WireGuard status API."""

    host: str
    session: ClientSession | None = None
    request_timeout: int = REQUEST_TIMEOUT

    async def _request(self, host: str) -> dict[str, Any]:
        """Handle a request to the wireGuard status API."""
        if self.session is None:
            self.session = ClientSession()

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.get(host)
        except TimeoutError as exc:
            msg: str = "Timeout occurred while connecting to WireGuard status API"
            raise WireGuardTimeoutError(msg) from exc

        if response.status != REQUIRED_STATUS:
            msg: str = "Unexpected status from WireGuard status API"
            raise WireGuardResponseError(msg, {"status": response.status})

        if (
            content_type := response.headers.get("content-type", "")
        ) != "application/json":
            text = await response.text()
            msg: str = "Unexpected content from WireGuard status API"
            raise WireGuardResponseError(
                msg, {"Content-Type": content_type, "response": text}
            )

        return await response.json()

    async def get_status(self) -> dict[str, Any]:
        """Get the WireGuard status."""
        return await self._request(self.host)

    async def get_peers(self) -> list[WireGuardPeer]:
        """Get the WireGuard status and convert to list of WireGuardPeer."""
        wg_status: dict[str, Any] = await self._request(self.host)
        return [WireGuardPeer.from_data(name, data) for name, data in wg_status.items()]

    async def close(self) -> None:
        """Close the client."""
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit."""
        await self.close()
