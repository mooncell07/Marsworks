from __future__ import annotations

import datetime
from typing import Optional, Union, List, Any

import httpx

from .origin import Camera, AlterRest, Rover, Serializer
from .manifest import Manifest
from .photo import Photo
from .origin.internal_utils import validate_cam

__all__ = (
    "AlterClient",
    "SyncClient",
)


class AlterClient:

    __slots__ = ("__http", "__session", "__sprswrngs")

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.Client] = None,
        suppress_warnings: bool = False,
    ) -> None:
        """
        AlterClient Constructor. (Alias: `SyncClient`)

        Use [Client](../API-Reference/client.md) for async usage.

        Arguments:

            api_key: NASA [API key](https://api.nasa.gov). (optional)
            session: A [Client](https://www.python-httpx.org/api/#client) object. (optional)
            suppress_warnings: Whether to suppress warnings.

        Warning:
            When api_key is not passed or it is `DEMO_KEY` a warning is sent. To suppress it
            `suppress_warnings` must be set to `True` explicitly.

        Hint:
            String input for the params. `name` and `camera` in this class's instance methods
            are internally converted to upper case to find the enum which is matching that input.

        """  # noqa: E501
        self.__http = AlterRest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )
        self.__session = session
        self.__sprswrngs = suppress_warnings

    def __enter__(self) -> AlterClient:
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close()

    def get_mission_manifest(self, name: Union[str, Rover]) -> Optional[Manifest]:
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
        serializer = self.__http.start(name.value)
        if serializer:
            return serializer.manifest_content()

    def get_photo_by_sol(
        self,
        name: Union[str, Rover],
        sol: Union[int, str],
        *,
        camera: Optional[Union[Camera, str]] = None,
        page: Optional[int] = None,
    ) -> Optional[List[Photo]]:
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
        camera = validate_cam(self.__sprswrngs, camera=camera)

        serializer = self.__http.start(
            name.value + "/photos", sol=sol, camera=camera, page=page
        )

        if serializer:
            return serializer.photo_content(self.__session)

    def get_photo_by_earthdate(
        self,
        name: Union[str, Rover],
        earth_date: Union[str, datetime.date],
        *,
        camera: Optional[Union[Camera, str]] = None,
        page: Optional[int] = None,
    ) -> Optional[List[Photo]]:
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
        camera = validate_cam(self.__sprswrngs, camera=camera)

        serializer = self.__http.start(
            name.name + "/photos", earth_date=str(earth_date), camera=camera, page=page
        )
        if serializer:
            return serializer.photo_content(self.__session)

    def get_latest_photo(
        self,
        name: Union[str, Rover],
        *,
        camera: Optional[Union[Camera, str]] = None,
        page: Optional[int] = None,
    ) -> Optional[List[Photo]]:
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
        camera = validate_cam(self.__sprswrngs, camera=camera)

        serializer = self.__http.start(
            name.name + "/latest_photos", camera=camera, page=page
        )
        if serializer:
            return serializer.photo_content(self.__session)

    def get_raw_response(self, path: str, **queries: Any) -> Optional[Serializer]:
        """
        Gets a [Serializer](./serializer.md) containing [Response](https://www.python-httpx.org/api/#response)
        of request made to
        API using `path` and `queries`.

        Args:

            path: The url path.
            queries: The endpoint to which call is to be made.

        Returns:

            A [Serializer](./serializer.md) object.

        """  # noqa: E501
        return self.__http.start(path, **queries)

    def close(self) -> None:
        """
        Closes the httpx.Client.

        Warning:
            It can close user given [Client](https://www.python-httpx.org/api/#client) too.
        """  # noqa: E501
        self.__http.close()


SyncClient = AlterClient  # Alias for easier understanding.
