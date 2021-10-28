"""
MIT License

Copyright (c) 2021 mooncell07

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import io
import warnings
from typing import Any, Mapping, Optional

import httpx
from rfc3986.builder import URIBuilder

from .exceptions import BadStatusCodeError, ContentTypeError
from .serializer import Serializer
from .tools import repr_gen


__all__ = (
    "AsyncRest",
    "SyncRest",
)


# Factory-like helper functions.
# ==============================================================================


def _checks(resp: httpx.Response) -> bool:
    """
    Checks status code and content type.
    """
    if not (300 > resp.status_code >= 200):
        raise BadStatusCodeError(resp)

    elif resp.headers["content-type"] not in (
        "application/json; charset=utf-8",
        "image/jpeg",
    ):
        raise ContentTypeError(resp)
    else:
        return True


def _build_url(base_url: str, path: str, queries: Mapping[str, Optional[str]]) -> str:
    """
    Builds the url.
    """
    queries = {k: v for k, v in queries.items() if v is not None}
    uri = URIBuilder(scheme="https", host=base_url, path="/" + path).add_query_from(
        queries
    )
    return uri.geturl()


# ==============================================================================


class AsyncRest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session: Optional[httpx.AsyncClient] = (
            session if isinstance(session, httpx.AsyncClient) else httpx.AsyncClient()
        )
        self._api_key = api_key or "DEMO_KEY"
        self._base_url = "api.nasa.gov/mars-photos/api/v1/rovers"
        self._suppress_warnings = suppress_warnings

    async def start(self, path: str, **params: Any) -> Optional[Serializer]:
        """
        Starts a http GET call.
        """
        if self._api_key == "DEMO_KEY" and not self._suppress_warnings:
            warnings.warn("Using DEMO_KEY for api call. Please use your api key.")

        params["api_key"] = self._api_key

        url = _build_url(self._base_url, path, params)

        resp = await self._session.get(url)  # type: ignore

        if _checks(resp):
            return Serializer(resp)

    async def read(self, url: str) -> Optional[io.BytesIO]:
        """
        Reads bytes of image.
        """
        resp = await self._session.get(url)  # type: ignore
        recon = await resp.aread()

        if _checks(resp):
            return io.BytesIO(recon)

    async def close(self) -> None:
        """
        Closes the AsyncClient and marks self._session as None.
        """
        if self._session is not None and isinstance(self._session, httpx.AsyncClient):
            self._session = await self._session.aclose()

    def __repr__(self):
        return repr_gen(self)


class SyncRest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.Client] = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session: Optional[httpx.Client] = (
            session if isinstance(session, httpx.Client) else httpx.Client()
        )
        self._api_key = api_key or "DEMO_KEY"
        self._base_url = "api.nasa.gov/mars-photos/api/v1/rovers"
        self._suppress_warnings = suppress_warnings

    def start(self, path: str, **params: Any) -> Optional[Serializer]:
        """
        Starts a http GET call.
        """
        if self._api_key == "DEMO_KEY" and not self._suppress_warnings:
            warnings.warn("Using DEMO_KEY for api call. Please use your api key.")

        params["api_key"] = self._api_key

        url = _build_url(self._base_url, path, params)

        resp = self._session.get(url)  # type: ignore

        if _checks(resp):
            return Serializer(resp)

    def read(self, url: str) -> Optional[io.BytesIO]:
        """
        Reads bytes of image.
        """
        resp = self._session.get(url)  # type: ignore
        recon = resp.read()

        if _checks(resp):
            return io.BytesIO(recon)

    def close(self) -> None:
        """
        Closes the Client and marks self._session as None.
        """
        if self._session is not None and isinstance(self._session, httpx.Client):
            self._session.close()

            self._session = None

    def __repr__(self):
        return repr_gen(self)
