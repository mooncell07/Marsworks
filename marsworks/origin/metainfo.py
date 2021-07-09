import aiohttp
from marsworks.origin.exceptions import BadContentError
from marsworks.manifest import Manifest
import marsworks
import inspect

__all__ = ("MetaInfo",)


class MetaInfo:

    __slots__ = ("_response",)

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self._response: aiohttp.ClientSession = response

    async def manifest_content(self) -> Manifest:
        """Serializes into Manifest."""
        data = (await self._response.json())["rover"]
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
            raise BadContentError(message=f"API returned <{data}> for this call.")

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"
