"""
MIT License

Copyright (c) 2021 NovaEmiya

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

from typing import Optional, Union
from os import PathLike
from io import BytesIO, IOBase, BufferedIOBase

import httpx
from rfc3986 import ParseResult, urlparse

from .origin.rest import Rest, AlterRest
from .partialmanifest import PartialManifest
from .origin.internal_utils import repr_gen

__all__ = ("Photo",)


class Photo:
    """
    A class representing a `Photo`.

    Attributes:

        photo_id (int): ID of the photo.
        sol (int): Sol when the photo was taken.
        img_src (str): Image url.
    """

    __slots__ = ("__http", "_data", "photo_id", "sol", "_camera", "img_src", "_rover")

    def __init__(self, data: dict, session: Union[Rest, AlterRest]):
        self.__http = (
            Rest(session=session)
            if isinstance(session, httpx.AsyncClient)
            else AlterRest(session=session)
        )
        self._data: dict = data
        self._camera: dict = data.get("camera", {})

        self.photo_id: Optional[int] = data.get("id")
        self.sol: Optional[int] = data.get("sol")
        self.img_src: Optional[str] = data.get("img_src")

    def __len__(self) -> int:
        """
        Returns:

            length of internal dict of attributes. (Result of `len(obj)`)
        """
        return len(self._data)

    def __str__(self) -> Optional[str]:
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

    def __hash__(self) -> int:
        """
        Returns:

            hash of the class. (Result of `hash(obj)`)
        """
        return hash(self.__class__)

    def __repr__(self) -> str:
        """
        Returns:

            Representation of Photo. (Result of `repr(obj)`)
        """
        return repr_gen(__class__, self)

    @property
    def rover(self) -> PartialManifest:
        """
        A [PartialManifest](./partialmanifest.md) object contatning some mission manifest of the rover.

        Returns:
            A [PartialManifest](./partialmanifest.md) object.
        """  # noqa: E501
        return PartialManifest(rover_info=self._data.get("rover", {}))

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
        return await self.__http.read(self.img_src)

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
        data = await self.__http.read(self.img_src)
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

        *Introduced in [v0.6.0](../changelog.md#v060).*
        """  # noqa: E501
        return self.__http.read(self.img_src)

    def save(self, fp: Union[str, bytes, PathLike, BufferedIOBase]) -> Optional[int]:
        """
        Saves the image.

        Arguments:

            fp: The file path (with name and extension) where the image has to be saved.

        Returns:

            Number of bytes written.

        *Introduced in [v0.6.0](../changelog.md#v060).*
        """
        data = self.__http.read(self.img_src)
        if data:
            if isinstance(fp, IOBase) and fp.writable():
                return fp.write(data.read1())
            else:
                with open(fp, "wb") as f:  # type: ignore
                    return f.write(data.read1())
