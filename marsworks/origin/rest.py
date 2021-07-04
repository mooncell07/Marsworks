import aiohttp
import typing
from marsworks.origin.exceptions import BadStatusCodeError, ContentTypeError
from marsworks.origin.base import Base

__all__ = ("Rest",)


class Rest:

    __slots__ = ("_session", "_api_key", "_base_url")

    def __init__(
        self, api_key: str, session: typing.Optional[aiohttp.ClientSession] = None
    ) -> None:
        self._session = session
        self._api_key = api_key
        self._base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/"

    async def _session_initializer(self) -> None:
        """
        initailizes a ClientSession if no (or bad) arg is
        passed to constructor.
        """
        self._session = aiohttp.ClientSession()

    async def start(self, rover: str, **params: typing.Any) -> aiohttp.ClientResponse:
        """
        starts an api call.
        """
        if not isinstance(self._session, aiohttp.ClientSession):
            await self._session_initializer()

        params.update(dict(api_key=self._api_key))

        resp = await self._session.get(self._base_url + rover, params=params)
        if not (300 > resp.status >= 200):
            raise BadStatusCodeError(resp)
        elif resp.content_type != "application/json":
            raise ContentTypeError(resp)
        else:
            return Base(resp)

    async def close(self) -> None:
        """
        Closes the ClientSession and marks session as None.
        """
        if self._session is not None:
            await self._session.close()
            self._session = None
