from __future__ import annotations

import datetime
import io
import os
from typing import Any, Optional, Union

import httpx

from .origin import BadArgumentError, Camera, Rest, Rover, Serializer
from .manifest import Manifest
from .photo import Photo

__all__ = ("Client",)


class Client:

    __slots__ = ("__http",)

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.AsyncClient] = None,
        suppress_warnings: bool = False,
    ) -> None:
        """
        Client Constructor.

        Arguments:
            api_key: NASA [API key](https://api.nasa.gov/). (optional)
            session: An [AsyncClient](https://www.python-httpx.org/api/#asyncclient) object. (optional)
            suppress_warnings: Whether to suppress warnings.

        Warning:
            When api_key is not passed or it is `DEMO_KEY` a warning is sent. To suppress it
            `suppress_warnings` must be set to `True` explicitly.
        """  # noqa: E501
        self.__http: Rest = Rest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self.close()

    async def get_mission_manifest(self, name: Union[str, Rover]) -> Optional[Manifest]:
        """
        Gets the mission manifest of this rover.

        Arguments:
            name : Name of rover.

        Note:
            `name` can be an enum of [Rover](../API-Reference/Enums/rover.md).

        Returns:
            A [Manifest](./manifest.md) object containing mission's info.
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        serializer = await self.__http.start(name.value)
        if serializer:
            return await serializer.manifest_content()

    async def get_photo_by_sol(
        self,
        name: Union[str, Rover],
        sol: Union[int, str],
        *,
        camera: Optional[str] = None,
        page: Optional[int] = None,
    ) -> Optional[list]:
        """
        Gets the photos taken by this rover on this sol.

        Arguments:
            name : Name of rover.
            sol: The sol when photo was captured.
            camera: Camera with which photo is taken. (Optional)
            page: The page number to look for. (25 items per page are returned)

        Note:
            `name` can be an enum of [Rover](../API-Reference/Enums/rover.md).
        Note:
            `camera` can be an enum of [Camera](../API-Reference/Enums/camera.md).

        Returns:
            A list of [Photo](./photo.md) objects with url and info.
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        if camera is not None:
            camera = (
                Camera(camera.upper()).value
                if camera.upper() in [type_.value for type_ in Camera]
                else None
            )

        serializer = await self.__http.start(
            name.value + "/photos", sol=sol, camera=camera, page=page
        )
        if serializer:
            return await serializer.photo_content()

    async def get_photo_by_earthdate(
        self,
        name: Union[str, Rover],
        earth_date: Union[str, datetime.date],
        *,
        camera: Optional[str] = None,
        page: Optional[int] = None,
    ) -> Optional[list]:
        """
        Gets the photos taken by this rover on this date.

        Arguments:
            name : Name of rover.
            earth_date: A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object or date in string form in YYYY-MM-DD format.
            camera: Camera with which photo is taken. (Optional)
            page: The page number to look for. (25 items per page are returned)

        Note:
            `name` can be an enum of [Rover](../API-Reference/Enums/rover.md).
        Note:
            `camera` can be an enum of [Camera](../API-Reference/Enums/camera.md).

        Returns:
            A list of [Photo](./photo.md) objects with url and info.
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        if camera is not None:
            camera = (
                Camera(camera.upper()).value
                if camera.upper() in [type_.value for type_ in Camera]
                else None
            )

        serializer = await self.__http.start(
            name.name + "/photos", earth_date=str(earth_date), camera=camera, page=page
        )
        if serializer:
            return await serializer.photo_content()

    async def get_latest_photo(
        self,
        name: Union[str, Rover],
        *,
        camera: Optional[str] = None,
        page: Optional[int] = None,
    ) -> Optional[list]:
        """
        Gets the latest photos taken by this rover.

        Arguments:
            name : Name of rover.
            camera: Camera with which photo is taken. (Optional)
            page: The page number to look for. (25 items per page are returned)

        Note:
            `name` can be an enum of [Rover](../API-Reference/Enums/rover.md).
        Note:
            `camera` can be an enum of [Camera](../API-Reference/Enums/camera.md).

        Returns:
            A list of [Photo](./photo.md) objects with url and info.

        *Introduced in [v0.3.0](../changelog.md#v030).*
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        if camera is not None:
            camera = (
                Camera(camera.upper()).value
                if camera.upper() in [type_.value for type_ in Camera]
                else None
            )

        serializer = await self.__http.start(
            name.name + "/latest_photos", camera=camera, page=page
        )
        if serializer:
            return await serializer.photo_content()

    async def read(self, photo: Photo) -> Optional[io.BytesIO]:
        """
        Reads the bytes of image url in photo.

        Arguments:
            photo : The [Photo](./photo.md) object whose image url is to be read.

        Returns:
            A [BytesIO](https://docs.python.org/3/library/io.html?highlight=bytesio#io.BytesIO) object.
        """  # noqa: E501
        if isinstance(photo, Photo):
            if photo.img_src:
                return await self.__http.read(photo.img_src)
        else:
            raise BadArgumentError("Photo", type(photo).__name__)

    async def save(
        self, photo: Photo, fp: Union[str, bytes, os.PathLike, io.BufferedIOBase]
    ) -> Optional[int]:
        """
        Saves the image of [Photo](./photo.md) object.

        Arguments:
            photo : The [Photo](./photo.md) object whose image is to be saved.
            fp: The file path (with name and extension) where the image has to be saved.

        Returns:
            Number of bytes written.
        """  # noqa: E501
        if isinstance(photo, Photo):
            if photo.img_src:
                bytes_ = await self.__http.read(photo.img_src)
                if bytes_:
                    if isinstance(fp, io.IOBase) and fp.writable():
                        return fp.write(bytes_.read1())
                    else:
                        with open(fp, "wb") as f:  # type: ignore
                            return f.write(bytes_.read1())
        else:
            raise BadArgumentError("Photo", type(photo).__name__)

    async def get_raw_response(self, path: str, **queries: Any) -> Optional[Serializer]:
        """
        Gets a [Serializer](./serializer.md) containing [Response](https://www.python-httpx.org/api/#response)
        of request made to
        API using `path` and `queries`.

        Args:
            path: The url path.
            queries: The endpoint to which call is to be made.

        Returns:
            A [Serializer](./serializer.md) object.

        *Introduced in [v0.4.0](../changelog.md#v040).*
        """  # noqa: E501
        return await self.__http.start(path, **queries)

    async def close(self) -> None:
        """
        Closes the AsyncClient.

        Warning:
            It can close user given [AsyncClient](https://www.python-httpx.org/api/#asyncclient) session too.
        """  # noqa: E501
        await self.__http.close()
