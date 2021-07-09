import aiohttp
from marsworks import Rest, Camera, Rover, Manifest, BadArgumentError, Photo
import typing
import datetime


__all__ = ("Client",)


class Client:

    __slots__ = ("__http",)

    def __init__(
        self,
        *,
        api_key: str = None,
        session: aiohttp.ClientSession = None,
        suppress_warnings: bool = False,
    ):
        self.__http = Rest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()

    async def get_mission_manifest(self, name: Rover) -> Manifest:
        if isinstance(name, Rover):
            metadata = await self.__http.start(name.name)
            mfst = await metadata.manifest_content()
            return mfst
        else:
            raise BadArgumentError(f"name should be a valid class variable of {Rover}.")

    async def get_photo_by_sol(
        self, name: Rover, sol: typing.Union[int, str], *, camera: Camera = None
    ):
        if isinstance(name, Rover):
            camera = camera.name if isinstance(camera, Camera) else None
            metadata = await self.__http.start(
                name.name + "/photos", sol=sol, camera=camera
            )
            phto = await metadata.photo_content()
            return phto
        else:
            raise BadArgumentError(f"name should be a valid class variable of {Rover}.")

    async def get_photo_by_earthdate(
        self, name: Rover, earth_date: datetime.date, *, camera: Camera = None
    ):
        if isinstance(name, Rover):
            camera = camera.name if isinstance(camera, Camera) else None
            metadata = await self.__http.start(
                name.name + "/photos", earth_date=str(earth_date), camera=camera
            )
            phto = await metadata.photo_content()
            return phto
        else:
            raise BadArgumentError(f"name should be a valid class variable of {Rover}.")

    async def read(self, photo: Photo):
        if isinstance(photo, Photo):
            data = await self.__http.read(photo.img_src)
            return data
        else:
            raise BadArgumentError(f"photo should be a valid instance of {Photo}.")

    async def close(self):
        await self.__http.close()
