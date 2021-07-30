import inspect
from typing import Optional

import httpx
import marsworks

from ..manifest import Manifest
from .exceptions import BadContentError

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

    def manifest_content(self) -> Manifest:
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

    def photo_content(self, session: Optional[None]) -> Optional[list]:
        """
        Serializes into a list of [Photo](./photo.md).

        Returns:

            A list of [Photo](./photo.md) objects with url and info.
        """
        data = self.response.json()
        options = ("photos", "latest_photos")

        data = {k: v for k, v in data.items() if k in options}

        if data and data[list(data)[0]]:
            return [marsworks.Photo(img, session) for img in data[list(data)[0]]]

        raise BadContentError(content=data)

    def __repr__(self):
        """
        Returns:

            Representation of Serializer. (Result of `repr(obj)`)
        """
        attrs = [
            attr
            for attr in inspect.getmembers(self)
            if not inspect.ismethod(attr[1])
            if not attr[0].startswith("_")
        ]
        fmt = ", ".join(f"{attr}={value}" for attr, value in attrs)[:-2]
        return f"{__class__.__name__}({fmt})"
