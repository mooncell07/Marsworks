import datetime
import io
import os
import typing
from typing import Union

import httpx

from marsworks import Camera, Manifest, Photo, Rest, Rover, ensure_type

__all__ = ("Client",)


class Client:

    __slots__ = ("__http",)

    def __init__(
        self,
        *,
        api_key: str = None,
        session: httpx.AsyncClient = None,
        suppress_warnings: bool = False,
    ):
        self.__http = Rest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    @ensure_type
    async def get_mission_manifest(self, name: Rover) -> Manifest:
        metadata = await self.__http.start(name.name)
        mfst = await metadata.manifest_content()
        return mfst

    @ensure_type
    async def get_photo_by_sol(
        self, name: Rover, sol: typing.Union[int, str], *, camera: Camera = None
    ):
        camera = camera.name if isinstance(camera, Camera) else None
        metadata = await self.__http.start(
            name.name + "/photos", sol=sol, camera=camera
        )
        phto = await metadata.photo_content()
        return phto

    @ensure_type
    async def get_photo_by_earthdate(
        self, name: Rover, earth_date: datetime.date, *, camera: Camera = None
    ):
        camera = camera.name if isinstance(camera, Camera) else None
        metadata = await self.__http.start(
            name.name + "/photos", earth_date=str(earth_date), camera=camera
        )
        phto = await metadata.photo_content()
        return phto

    @ensure_type
    async def read(self, photo: Photo, bytes_: bool = False):
        data = await self.__http.read(photo.img_src, bytes_=bytes_)
        return data

    @ensure_type
    async def save(
        self, photo: Photo, fp: Union[str, bytes, os.PathLike, io.BufferedIOBase]
    ):
        read_data = await self.__http.read(photo.img_src, bytes_=True)
        if isinstance(fp, io.IOBase) and fp.writable():
            bw = fp.write(read_data)
            return bw
        else:
            with open(fp, "wb") as f:
                return f.write(read_data)

    async def close(self):
        await self.__http.close()
