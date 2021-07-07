import aiohttp
import typing
from marsworks.origin.exceptions import BadStatusCodeError, ContentTypeError
from marsworks.origin.metainfo import MetaInfo
import warnings
import inspect

__all__ = ("Rest",)


class Rest:

    __slots__ = ("_session", "_api_key", "_base_url", "_suppress_warnings")

    def __init__(
        self,
        *,
        api_key: str = "DEMO_KEY",
        session: typing.Optional[aiohttp.ClientSession] = None,
        suppress_warnings: bool = False,
    ) -> None:
        self._session = session
        self._api_key = api_key
        self._base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers"
        self._suppress_warnings = suppress_warnings

    async def _session_initializer(self) -> None:
        """
        Initailizes a ClientSession if no (or bad) arg is
        passed to constructor.
        """
        self._session = aiohttp.ClientSession()

    async def start(self, path: str, **params: typing.Any) -> MetaInfo:
        """
        Starts an api call.
        """
        if not isinstance(self._session, aiohttp.ClientSession):
            await self._session_initializer()

        params.update(dict(api_key=self._api_key))
        if self._api_key == "DEMO_KEY" and not self._suppress_warnings:
            warnings.warn("Using DEMO_KEY for api call. Please use your api key.")
        resp = await self._session.get(self._base_url + path, params=params)
        if not (300 > resp.status >= 200):
            raise BadStatusCodeError(resp)
        elif resp.content_type != "application/json":
            raise ContentTypeError(resp)
        else:
            return MetaInfo(resp)
        await self.close()

    async def close(self) -> None:
        """
        Closes the ClientSession and marks session as None.
        """
        if self._session is not None:
            await self._session.close()
            self._session = None

    def __repr__(self):
        form = ""
        items = filter(lambda a: not a[0].startswith("_"), inspect.getmembers(self))

        for i in items:
            form += f"{i[0]} = {i[1]}, "
        return f"{self.__class__.__name__}({form[:-2]})"
