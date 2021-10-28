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

from typing import Optional, Union, Mapping, Any
from os import PathLike
from io import BytesIO, IOBase, BufferedIOBase

import httpx
from rfc3986 import ParseResult, urlparse

from .origin.rest import AsyncRest, SyncRest
from .partialmanifest import PartialManifest
from .origin.exceptions import BadContentError
from .origin.tools import repr_gen

__all__ = ("Photo",)


class Photo:
    """
    A class representing a `Photo`.

    Attributes:

        photo_id (int): ID of the photo.
        sol (int): Sol when the photo was taken.
        img_src (str): Image url. Defaults to medium size for Curiosity, Opportunity,
        Spirit. Defaults to large size for Perseverance.
    """

    __slots__ = ("_session", "_data", "sol", "_camera", "_rover", "img_src", "photo_id")

    def __init__(
        self,
        data: Mapping[str, Any],
        session: Optional[Union[httpx.AsyncClient, httpx.Client]],
    ):
        self._session = session
        self._data = data
        self._camera: Mapping[Any, Any] = data.get("camera", {})

        self.photo_id: Optional[int] = data.get("id")
        self.sol: Optional[int] = data.get("sol")
        self.img_src: str = data["img_src"]

    def __len__(self) -> int:
        """
        Returns:

            length of internal dict of attributes. (Result of `len(obj)`)
        """
        return len(self._data)

    def __str__(self) -> str:
        """
        Returns:

            url of image. (Result of `str(obj)`)
        """
        return self.img_src

    def __eq__(self, value) -> bool:
        """
        Checks if two objects are same using `photo_id`.

        Returns:

            Result of `obj == obj`.
        """
        return isinstance(value, self.__class__) and value.photo_id == self.photo_id

    def __repr__(self) -> str:
        """
        Returns:

            Representation of Photo. (Result of `repr(obj)`)
        """
        return repr_gen(self)

    @property
    def rover(self) -> PartialManifest:
        """
        A [PartialManifest](./partialmanifest.md) object contatning some mission manifest of the rover.

        Returns:
            A [PartialManifest](./partialmanifest.md) object.
        """  # noqa: E501
        try:
            return PartialManifest(rover_info=self._data["rover"])
        except KeyError:
            raise BadContentError(
                message="No data available for building PartialManifest."
            ) from None

    @property
    def camera_id(self) -> Optional[int]:
        """
        ID of camera with which photo was taken.

        Returns:

            The id as an integer.
        """
        return self._camera.get("id")

    @property
    def camera_name(self) -> Optional[str]:
        """
        Name of camera with which photo was taken.

        Returns:

            The name as a string.
        """
        return self._camera.get("name")

    @property
    def camera_rover_id(self) -> Optional[int]:
        """
        Rover id on which this camera is present.

        Returns:

            The rover id as an integer.
        """
        return self._camera.get("rover_id")

    @property
    def camera_full_name(self) -> Optional[str]:
        """
        Full-Name of camera with which photo was taken.

        Returns:

            The full-name as a string.
        """
        return self._camera.get("full_name")

    def parse_img_src(self) -> ParseResult:
        """
        Parses the image URL.

        Returns:

            A [ParseResult](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.ParseResult)-like object.

        *Introduced in [v0.3.0](../changelog.md#v030).*
        """  # noqa: E501

        return urlparse(self.img_src)

    async def aread(self) -> Optional[BytesIO]:
        """
        Reads the bytes of image asynchronously.

        Returns:

            A [BytesIO](https://docs.python.org/3/library/io.html?highlight=bytesio#io.BytesIO) object.

        *Introduced in [v0.5.0](../changelog.md#v050).*
        """  # noqa: E501
        http = AsyncRest(session=self._session)  # type: ignore
        data = await http.read(self.img_src)
        await http.close()
        return data

    async def asave(
        self, fp: Union[str, bytes, PathLike, BufferedIOBase]
    ) -> Optional[int]:
        """
        Saves the image asynchronously.

        Arguments:

            fp: The file path (with name and extension) where the image has to be saved.

        Returns:

            Number of bytes written.

        *Introduced in [v0.5.0](../changelog.md#v050).*
        """
        data = await self.aread()
        if data:
            if isinstance(fp, IOBase) and fp.writable():
                return fp.write(data.read1())
            else:
                with open(fp, "wb") as f:  # type: ignore
                    return f.write(data.read1())

    def read(self) -> Optional[BytesIO]:
        """
        Reads the bytes of image.

        Returns:

            A [BytesIO](https://docs.python.org/3/library/io.html?highlight=bytesio#io.BytesIO) object.

        Warning:
            Do **NOT** use this inside a coroutine function. Check this
            [question](../faq.md#q6-why-cant-i-use-photosave-or-photoread-in-coroutine-functions).

        *Introduced in [v0.6.0](../changelog.md#v060).*
        """  # noqa: E501
        http = SyncRest(session=self._session)  # type: ignore
        data = http.read(self.img_src)
        http.close()
        return data

    def save(self, fp: Union[str, bytes, PathLike, BufferedIOBase]) -> Optional[int]:
        """
        Saves the image.

        Arguments:

            fp: The file path (with name and extension) where the image has to be saved.

        Returns:

            Number of bytes written.

        *Introduced in [v0.6.0](../changelog.md#v060).*
        """
        data = self.read()
        if data:
            if isinstance(fp, IOBase) and fp.writable():
                return fp.write(data.read1())
            else:
                with open(fp, "wb") as f:  # type: ignore
                    return f.write(data.read1())
