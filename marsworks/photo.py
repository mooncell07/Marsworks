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

from rfc3986 import ParseResult, urlparse  # type: ignore

from .origin.rest import AsyncRest, SyncRest
from .partialmanifest import PartialManifest
from .origin.exceptions import BadContentError, MarsworksError
from .origin.tools import repr_gen

__all__ = ("Photo",)


class Photo:
    """
    A class representing a `Photo`.

    Attributes:
        photo_id (Optional[int]): ID of the photo.
        sol (Optional[int]): Sol when the photo was taken.
        img_src (str): Image url.

    Info:
        Images default to medium size for Curiosity, Opportunity &
        Spirit and large size for Perseverance.
    """

    __slots__ = ("_http", "_data", "sol", "_camera", "_rover", "img_src", "photo_id")

    def __init__(
        self,
        data: Mapping[str, Any],
        http: Union[AsyncRest, SyncRest],
    ) -> None:
        self._http = http
        self._data = data
        self._camera: Mapping[Any, Any] = data.get("camera", {})

        self.photo_id: Optional[int] = data.get("id")
        self.sol: Optional[int] = data.get("sol")
        self.img_src: str = data["img_src"]

    def __len__(self) -> int:
        """
        Returns:
            length of internal [dict][] of attributes. (Result of `len(obj)`)
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
    def _verify_async_session_integrity(self) -> bool:
        if isinstance(self._http, AsyncRest):
            return True
        else:
            return False

    @property
    def rover(self) -> PartialManifest:
        """
        A [PartialManifest](./partialmanifest.md) object containing some mission manifest of the rover.

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
            The id as an [int][].
        """
        return self._camera.get("id")

    @property
    def camera_name(self) -> Optional[str]:
        """
        Name of camera with which photo was taken.

        Returns:
            The name as a [str][].
        """
        return self._camera.get("name")

    @property
    def camera_rover_id(self) -> Optional[int]:
        """
        Rover id on which this camera is present.

        Returns:
            The rover id as an [int][].
        """
        return self._camera.get("rover_id")

    @property
    def camera_full_name(self) -> Optional[str]:
        """
        Full Name of camera with which photo was taken.

        Returns:
            The full-name as a [str][].
        """
        return self._camera.get("full_name")

    def parse_img_src(self) -> ParseResult:
        """
        Parses the image URL.

        Returns:
            A [urllib.parse.ParseResult][]-like object.

        *Introduced in [v0.3.0](../changelog.md#v030).*
        """  # noqa: E501

        return urlparse(self.img_src)

    async def aread(self) -> Optional[BytesIO]:
        """
        Reads the bytes of image asynchronously.

        Returns:
            A [io.BytesIO][] object.

        *Introduced in [v0.5.0](../changelog.md#v050).*
        """  # noqa: E501
        if self._verify_async_session_integrity:
            data = await self._http.read(self.img_src)  # type: ignore
            return data
        else:
            raise MarsworksError(
                "This object doesn't support async. HTTP requests."
            ) from None

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
            A [io.BytesIO][] object.

        Warning:
            Do **NOT** use this inside a coroutine function. Check this
            [question](../faq.md#q6-why-cant-i-use-photosave-or-photoread-in-coroutine-functions).

        *Introduced in [v0.6.0](../changelog.md#v060).*
        """  # noqa: E501
        if not self._verify_async_session_integrity:
            data = self._http.read(self.img_src)
            return data  # type: ignore
        else:
            raise MarsworksError(
                "This object doesn't support sync. HTTP requests."
            ) from None

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
