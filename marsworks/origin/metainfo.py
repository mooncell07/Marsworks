import aiohttp
from marsworks.origin.exceptions import BadContentError
from marsworks.manifest import Manifest
import marsworks
import inspect

__all__ = ("MetaInfo",)


class MetaInfo:

    __slots__ = ("_response", "url", "status", "ok", "headers")

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self._response: aiohttp.ClientSession = response
        self.url: str = response.url
        self.status: int = response.status
        self.ok: bool = response.ok
        self.headers: dict = response.headers

    async def manifest_content(self) -> Manifest:
        """Serializes into Manifest."""
        data = (await self._response.json())["Error"]
        if data != []:
            return Manifest(data)
        else:
            raise BadContentError(content=data)

    async def photo_content(self) -> list:
        """Serializes into Photo."""
        data = (await self._response.json())["photos"]
        if data != []:
            return [marsworks.Photo(img) for img in data]
        else:
            raise BadContentError(content=data)

    def __repr__(self):
        form = ""
        items = filter(lambda a: not a[0].startswith("_"), inspect.getmembers(self))

        for i in items:
            form += f"{i[0]} = {i[1]}, "
        return f"{self.__class__.__name__}({form[:-2]})"
