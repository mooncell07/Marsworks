import aiohttp
import typing
from marsworks.origin.exceptions import BadStatusCodeError, ContentTypeError
from marsworks.origin.metainfo import MetaInfo
import warnings
import inspect
import yarl
import io

__all__ = ("Rest",)


class Rest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: str = None,
        session: aiohttp.ClientSession = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session = session
        self._api_key = api_key or "DEMO_KEY"
        self._base_url = "api.nasa.gov/mars-photos/api/v1/rovers"
        self._suppress_warnings = suppress_warnings

    async def _session_initializer(self) -> None:
        """
        Initailizes a ClientSession if no (or bad) session arg is
        passed to constructor.
        """
        self._session = aiohttp.ClientSession()

    async def start(self, path: str, **params: typing.Any) -> MetaInfo:
        """
        Starts an api call.
        """
        if not isinstance(self._session, aiohttp.ClientSession):
            await self._session_initializer()
        params["api_key"] = self._api_key
        if self._api_key == "DEMO_KEY" and not self._suppress_warnings:
            warnings.warn("Using DEMO_KEY for api call. Please use your api key.")

        url = self._build_url(path, params)

        resp = await self._session.get(str(url))

        if self._checks(resp):
            return MetaInfo(resp)

    async def read(self, url: str) -> io.BytesIO:
        resp = await self._session.get(url)
        if self._checks(resp):
            return io.BytesIO(await resp.read())

    # ===========Factory-like helper methods.================================
    def _checks(self, resp: aiohttp.ClientResponse) -> bool:
        if not (300 > resp.status >= 200):
            raise BadStatusCodeError(resp)
        elif resp.content_type not in ("application/json", "image/jpeg"):
            raise ContentTypeError(resp)
        else:
            return True

    def _build_url(self, path: str, queries: dict) -> yarl.URL:
        for q in list(queries):
            if queries[q] is None:
                queries.pop(q)
        url = yarl.URL.build(
            scheme="https", host=self._base_url, path="/" + path, query=queries
        )
        return url

    # =========================================================================

    async def close(self) -> None:
        """
        Closes the ClientSession and marks self.session as None.
        """
        if self._session is not None:
            await self._session.close()
            self._session = None

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"
