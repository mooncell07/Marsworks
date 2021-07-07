import aiohttp
from marsworks.origin.exceptions import BadContentError
from marsworks.manifest import Manifest

__all__ = ("Parser",)


class Parser:

    __slots__ = ("_response", "url", "status", "ok", "headers")

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self._response: aiohttp.ClientSession = response
        self.url: str = response.url
        self.status: int = response.status
        self.ok: bool = response.ok
        self.headers: dict = response.headers

    async def manifest_content(self) -> Manifest:
        """Serializes into Manifest."""
        data = await self._response.json()
        try:
            data = data["rover"]
        except KeyError:
            raise BadContentError(content=data) from None
        return Manifest(data)

    def __repr__(self):
        form = ""
        items = {s: getattr(self, s) for s in self.__class__.__slots__}
        for i in items:
            form += f"{i} = {items[i]}, "
        return f"{self.__class__.__name__}({form})"
