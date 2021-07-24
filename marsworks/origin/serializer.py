import inspect

import httpx
import marsworks
from marsworks.manifest import Manifest
from marsworks.origin.exceptions import BadContentError

__all__ = ("Serializer",)


class Serializer:
    """
    A class representing a Serializer, used for serializing response into
    other objects.

    Attributes:
        response (httpx.Response): The response API returned.

    Warning:
        This object is not for public use unless `await Client.get_raw_response()`
        is being used.
    """

    __slots__ = ("response",)

    def __init__(self, response: httpx.Response) -> None:
        self.response = response

    async def manifest_content(self) -> Manifest:
        """
        Serializes into [Manifest](./manifest.md).

        Returns:
            A [Manifest](./manifest.md) object containing mission's info.
        """
        data = (self.response.json())["rover"]
        if data:
            return Manifest(data)
        else:
            raise BadContentError(content=data)

    async def photo_content(self) -> list:
        """
        Serializes into a list of [Photo](./photo.md).

        Returns:
            A list of [Photo](./photo.md) objects with url and info.
        """
        data = self.response.json()
        for key in data:
            if key in ("photos", "latest_photos"):
                data = data[key]
        if data != []:
            return [marsworks.Photo(img) for img in data]
        return data

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"
