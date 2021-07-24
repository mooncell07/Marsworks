import inspect
import io
import warnings
from typing import Any, Optional

import httpx
from rfc3986.builder import URIBuilder

from .exceptions import BadStatusCodeError, ContentTypeError
from .serializer import Serializer

__all__ = ("Rest",)


class Rest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session = session or httpx.AsyncClient()
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
        url = self._build_url(path, params)

        resp = await self._session.get(url)  # type: ignore

        if self._checks(resp):
            return Serializer(resp)

    async def read(self, url: str) -> Optional[io.BytesIO]:
        """
        Reads bytes of image.
        """
        resp = await self._session.get(url)  # type: ignore
        recon = await resp.aread()

        if self._checks(resp):
            return io.BytesIO(recon)

    # ===========Factory-like helper methods.================================
    def _checks(self, resp: httpx.Response) -> bool:
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

    def _build_url(self, path: str, queries: dict) -> str:
        """
        Builds the url.
        """
        queries = {k: v for k, v in queries.items() if v is not None}
        uri = URIBuilder(
            scheme="https", host=self._base_url, path="/" + path
        ).add_query_from(queries)
        return uri.geturl()

    # =========================================================================

    async def close(self) -> None:
        """
        Closes the AsyncClient and marks self.session as None.
        """
        if self._session is not None and isinstance(self._session, httpx.AsyncClient):
            self._session = await self._session.aclose()

    def __repr__(self):
        attrs = [
            attr
            for attr in inspect.getmembers(self)
            if not inspect.ismethod(attr[1])
            if not attr[0].startswith("_")
        ]
        fmt = ", ".join(f"{attr}={value}" for attr, value in attrs)[:-2]
        return f"{__class__.__name__}({fmt})"
