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

from __future__ import annotations

import datetime
from typing import Optional, Union, List, Mapping

import httpx

from .origin import Camera, SyncRest, Rover, Serializer
from .manifest import Manifest
from .photo import Photo
from .origin.internal_utils import validate_cam

__all__ = ("SyncClient",)


class SyncClient:

    __slots__ = ("_http", "_session", "_sprswrngs")

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        session: Optional[httpx.Client] = None,
        suppress_warnings: bool = False,
    ) -> None:
        """
        SyncClient Constructor.

        Use [Client](../API-Reference/asyncclient.md) for async requests.

        Arguments:

            api_key: NASA [API key](https://api.nasa.gov). (optional)
            session: A [Client](https://www.python-httpx.org/api/#client) object. (optional)
            suppress_warnings: Whether to suppress warnings.

        Warning:
            When api_key is not passed or it is `DEMO_KEY` a warning is sent. To suppress it
            `suppress_warnings` must be set to `True` explicitly.

        Hint:
            For `name` and `camera` param. of this class's instance methods you can pass enums
            [Rover](../API-Reference/Enums/rover.md) and [Camera](../API-Reference/Enums/camera.md).
            You can also pass args as string.

        """  # noqa: E501
        self._http: SyncRest = SyncRest(
            api_key=api_key, session=session, suppress_warnings=suppress_warnings
        )
        self._session = session
        self._sprswrngs = suppress_warnings

    def __enter__(self) -> SyncClient:
        return self

    def __exit__(self, type, value, tb) -> None:
        self.close()

    def get_mission_manifest(self, name: Union[str, Rover]) -> Optional[Manifest]:
        """
        Gets the mission manifest of this rover.

        Arguments:

            name : Name of rover.

        Returns:

            A [Manifest](./manifest.md) object containing mission's info.
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        serializer = self._http.start(name.value)
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

        Returns:

            A list of [Photo](./photo.md) objects with url and info.
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        camera = validate_cam(self._sprswrngs, camera=camera)

        serializer = self._http.start(
            name.value + "/photos", sol=sol, camera=camera, page=page
        )

        if serializer:
            return serializer.photo_content(self._session)

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

        Returns:

            A list of [Photo](./photo.md) objects with url and info.
        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        camera = validate_cam(self._sprswrngs, camera=camera)

        serializer = self._http.start(
            name.name + "/photos", earth_date=str(earth_date), camera=camera, page=page
        )
        if serializer:
            return serializer.photo_content(self._session)

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

        Returns:

            A list of [Photo](./photo.md) objects with url and info.

        """  # noqa: E501
        name = Rover(name.upper() if isinstance(name, str) else name)
        camera = validate_cam(self._sprswrngs, camera=camera)

        serializer = self._http.start(
            name.name + "/latest_photos", camera=camera, page=page
        )
        if serializer:
            return serializer.photo_content(self._session)

    def get_raw_response(
        self, path: str, **queries: Mapping[str, str]
    ) -> Optional[Serializer]:
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
        return self._http.start(path, **queries)

    def close(self) -> None:
        """
        Closes the SyncClient.

        Warning:
            It can close user given [Client](https://www.python-httpx.org/api/#client) session too.
        """  # noqa: E501
        self._http.close()
