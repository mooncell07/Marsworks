"""
MIT License

Copyright (c) 2021 mooncell07

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Optional

import httpx


import marsworks
from ..manifest import Manifest
from .exceptions import BadContentError
from .internal_utils import repr_gen

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

    def manifest_content(self) -> Optional[Manifest]:
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

    def __repr__(self) -> str:
        """
        Returns:

            Representation of Serializer. (Result of `repr(obj)`)
        """
        return repr_gen(__class__, self)
