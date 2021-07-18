import datetime
import io
import os
from typing import Union, Optional

import httpx

from marsworks.origin import Rest, Camera, Rover, BadArgumentError
from marsworks.manifest import Manifest
from marsworks.photo import Photo

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
        """  # noqa: E501
        self.__http: Rest = Rest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    async def get_mission_manifest(self, name: Union[str, Rover]) -> Manifest:
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

        slz = await self.__http.start(name.value)
        mfst = await slz.manifest_content()

        return mfst

    async def get_photo_by_sol(
        self,
        name: Union[str, Rover],
        sol: Union[int, str],
        *,
        camera: Optional[str] = None,
        page: Optional[int] = None,
    ) -> list:
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

        try:
            camera = Camera(camera.upper() if isinstance(camera, str) else camera).value
        except ValueError:
            camera = None

        slz = await self.__http.start(
            name.value + "/photos", sol=sol, camera=camera, page=page
        )
        pht = await slz.photo_content()

        return pht

    async def get_photo_by_earthdate(
        self,
        name: Union[str, Rover],
        earth_date: Union[str, datetime.date],
        *,
        camera: Optional[str] = None,
        page: Optional[int] = None,
    ) -> list:
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

        try:
            camera = Camera(camera.upper() if isinstance(camera, str) else camera).value
        except ValueError:
            camera = None

        slz = await self.__http.start(
            name.name + "/photos", earth_date=str(earth_date), camera=camera, page=page
        )
        pht = await slz.photo_content()

        return pht

    async def get_latest_photos(
        self,
        name: Union[str, Rover],
        *,
        camera: Optional[str] = None,
        page: Optional[int] = None,
    ) -> list:
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
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)

        try:
            camera = Camera(camera.upper() if isinstance(camera, str) else camera).value
        except ValueError:
            camera = None

        slz = await self.__http.start(
            name.name + "/latest_photos", camera=camera, page=page
        )
        pht = await slz.photo_content()

        return pht

    async def read(self, photo: Photo) -> io.BytesIO:
        """
        Reads the bytes of image url in photo.

        Arguments:
            photo : The [Photo](./photo.md) object whose image url is to be read.

        Returns:
            A [BytesIO](https://docs.python.org/3/library/io.html?highlight=bytesio#io.BytesIO) object.
        """  # noqa: E501
        if isinstance(photo, Photo):
            bio = await self.__http.read(photo.img_src)

            return bio

        else:
            raise BadArgumentError("Photo", type(photo).__name__)

    async def save(
        self, photo: Photo, fp: Union[str, bytes, os.PathLike, io.BufferedIOBase]
    ) -> int:
        """
        Saves the image of [Photo](./photo.md) object.

        Arguments:
            photo : The [Photo](./photo.md) object whose image is to be saved.
            fp: The file path (with name and extension) where the image has to be saved.

        Returns:
            Number of bytes written.
        """  # noqa: E501
        if isinstance(photo, Photo):
            bio = await self.__http.read(photo.img_src)

            if isinstance(fp, io.IOBase) and fp.writable():
                bw = fp.write(bio.read1())

                return bw

            else:
                with open(fp, "wb") as f:

                    return f.write(bio.read1())

        else:
            raise BadArgumentError("Photo", type(photo).__name__)

    async def close(self) -> None:
        """
        Closes the AsyncClient.

        Warning:
            It can close user given [AsyncClient](https://www.python-httpx.org/api/#asyncclient) session too.
        """  # noqa: E501
        await self.__http.close()
