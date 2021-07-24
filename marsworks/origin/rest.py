import inspect
from typing import Optional, Any
import warnings
import io

import httpx
from marsworks.origin.exceptions import BadStatusCodeError, ContentTypeError
from marsworks.origin.serializer import Serializer
from rfc3986.builder import URIBuilder

__all__ = ("Rest",)


class MISSING:
    def get(*args, **kwargs):
        ...

class Rest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session = session if isinstance(session, httpx.AsyncClient) else httpx.AsyncClient()
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

        resp = await self._session.get(url) # type: ignore

        if self._checks(resp):
            return Serializer(resp)
        return None

    async def read(self, url: str) -> Optional[io.BytesIO]:
        """
        Reads bytes of image.
        """
        resp = await self._session.get(url) # type: ignore
        recon = await resp.aread()

        if self._checks(resp):
            return io.BytesIO(recon)
        return None

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
        for q in list(queries):
            if queries[q] is None:
                queries.pop(q)

        url = URIBuilder(
            scheme="https", host=self._base_url, path="/" + path
        ).add_query_from(queries)
        return url.geturl()

    # =========================================================================

    async def close(self) -> None:
        """
        Closes the AsyncClient and marks self.session as None.
        """
        if self._session is not None and isinstance(self._session, httpx.AsyncClient):
            self._session = await self._session.aclose()

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"
