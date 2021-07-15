import inspect
import io
import typing
import warnings

import httpx
from marsworks.origin.exceptions import BadStatusCodeError, ContentTypeError
from marsworks.origin.metainfo import MetaInfo
from rfc3986.builder import URIBuilder

__all__ = ("Rest",)


class Rest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: str = None,
        session: httpx.AsyncClient = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session = session
        self._api_key = api_key or "DEMO_KEY"
        self._base_url = "api.nasa.gov/mars-photos/api/v1/rovers"
        self._suppress_warnings = suppress_warnings

    async def _session_initializer(self) -> None:
        """
        Initailizes an AsyncClient if no (or bad) session arg is
        passed to constructor.
        """
        self._session = httpx.AsyncClient()

    async def start(self, path: str, **params: typing.Any) -> MetaInfo:
        """
        Starts an api call.
        """
        if not isinstance(self._session, httpx.AsyncClient):
            await self._session_initializer()
        params["api_key"] = self._api_key

        if self._api_key == "DEMO_KEY" and not self._suppress_warnings:
            warnings.warn("Using DEMO_KEY for api call. Please use your api key.")

        url = self._build_url(path, params)

        resp = await self._session.get(url)

        if self._checks(resp):
            return MetaInfo(resp)

    async def read(
        self, url: str, bytes_: bool = False
    ) -> typing.Union[io.BytesIO, bytes]:
        """
        Reads bytes of image.
        """
        if not isinstance(self._session, httpx.AsyncClient):
            await self._session_initializer()
        resp = await self._session.get(url)
        recon = await resp.aread()
        if self._checks(resp):
            if bytes_:
                return recon
            return io.BytesIO(recon)

    # ===========Factory-like helper methods.================================
    def _checks(self, resp: httpx.AsyncClient) -> bool:
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
        if self._session is not None:
            await self._session.aclose()
            self._session = None

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"
