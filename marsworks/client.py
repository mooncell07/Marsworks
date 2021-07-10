import datetime
import io
import os
import typing
from typing import Union

import httpx

from marsworks.origin import Rest, Camera, Rover, ensure_type
from marsworks.manifest import Manifest
from marsworks.photo import Photo

__all__ = ("Client",)


class Client:

    __slots__ = ("__http",)

    def __init__(
        self,
        *,
        api_key: str = None,
        session: httpx.AsyncClient = None,
        suppress_warnings: bool = False,
    ) -> None:
        """
        Client Constructor.

        Arguments:
            api_key: NASA [API key](https://api.nasa.gov/). (optional)
            session: An [AsyncClient](https://www.python-httpx.org/api/#asyncclient) object. (optional)
            suppress_warnings: Whether to suppress warnings.
        """  # noqa: E501
        self.__http = Rest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    @ensure_type
    async def get_mission_manifest(self, name: Rover) -> Manifest:
        """
        Gets the mission manifest of the rover passed in `name` arg.

        Arguments:
            name : Name of rover. Must be an enum of [Rover](/marsworks/enums/#Rover).

        Returns:
            A [Manifest](/marsworks/#Manifest) object containing mission's info
        """  # noqa: E501
        metadata = await self.__http.start(name.name)
        mfst = await metadata.manifest_content()
        return mfst

    @ensure_type
    async def get_photo_by_sol(
        self, name: Rover, sol: typing.Union[int, str], *, camera: Camera = None
    ) -> list:
        """
        Gets the photos taken by the given rover on the given sol.
        We can sort the images with `camera` param.

        Arguments:
            name : Name of rover. Must be an enum of [Rover](/marsworks/enums/#Rover).
            sol: Union[int, str]
            camera: Camera with which photo is taken. Must be an enum of [Camera](/marsworks/enums/#Camera).

        Returns:
            A list of [Photo](/marsworks/#Manifest) objects with url and info.
        """  # noqa: E501
        camera = camera.name if isinstance(camera, Camera) else None
        metadata = await self.__http.start(
            name.name + "/photos", sol=sol, camera=camera
        )
        phto = await metadata.photo_content()
        return phto

    @ensure_type
    async def get_photo_by_earthdate(
        self, name: Rover, earth_date: datetime.date, *, camera: Camera = None
    ) -> list:
        """
        Gets the photos taken by the given rover on the given date.
        We can sort the images with `camera` param.

        Arguments:
            name : Name of rover. Must be an enum of [Rover](/marsworks/enums/#Rover).
            earth_date: [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date)
            camera: Camera with which photo is taken. Must be an enum of [Camera](/marsworks/enums/#Camera).

        Returns:
            A list of [Photo](/marsworks/#Manifest) objects with url and info.
        """  # noqa: E501
        camera = camera.name if isinstance(camera, Camera) else None
        metadata = await self.__http.start(
            name.name + "/photos", earth_date=str(earth_date), camera=camera
        )
        phto = await metadata.photo_content()
        return phto

    @ensure_type
    async def read(self, photo: Photo) -> io.BytesIO:
        """
        Reads the bytes of image url in photo.

        Arguments:
            photo : The [Photo](/marsworks/photo/#Photo) object whose image url is to be read.

        Returns:
            An [io.BytesIO](https://docs.python.org/3/library/io.html?highlight=bytesio#io.BytesIO) object.
        """  # noqa: E501
        data = await self.__http.read(photo.img_src)
        return data

    @ensure_type
    async def save(
        self, photo: Photo, fp: Union[str, bytes, os.PathLike, io.BufferedIOBase]
    ) -> int:
        """
        Saves the image of [Photo](/marsworks/photo/#Photo) object.

        Arguments:
            photo : The [Photo](/marsworks/photo/#Photo) object whose image is to be saved.
            fp: The file path (with name and extension) where the image has to be saved.

        Returns:
            Number of bytes written.
        """  # noqa: E501
        read_data = await self.__http.read(photo.img_src, bytes_=True)
        if isinstance(fp, io.IOBase) and fp.writable():
            bw = fp.write(read_data)
            return bw
        else:
            with open(fp, "wb") as f:
                return f.write(read_data)

    async def close(self) -> None:
        """
        Closes the AsyncClient.

        Warning:
            It can close user given [AsyncClient](https://www.python-httpx.org/api/#asyncclient) session too.
        """  # noqa: E501
        await self.__http.close()
