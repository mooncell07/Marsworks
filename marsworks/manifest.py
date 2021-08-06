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

from datetime import date, datetime
from typing import Optional

from .origin.exceptions import BadContentError
from .origin.internal_utils import repr_gen

__all__ = ("Manifest",)


class Manifest:
    """
    A class representing a `Manifest`.

    Attributes:

        rover_id (int): ID of the rover.
        name (str): Name of the Rover.
        status (str): The Rover's mission status.
        max_sol (int): The most recent Martian sol from which photos exist.
        total_photos (int): Number of photos taken by that Rover.
        cameras (dict): Cameras for which there are photos by that Rover on that sol.
    """

    __slots__ = (
        "_data",
        "rover_id",
        "name",
        "status",
        "max_sol",
        "total_photos",
        "cameras",
    )

    def __init__(self, data: dict) -> None:
        self._data: dict = data
        self.rover_id: Optional[int] = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.status: Optional[str] = data.get("status")
        self.max_sol: Optional[int] = data.get("max_sol")
        self.total_photos: Optional[int] = data.get("total_photos")
        self.cameras: Optional[dict] = data.get("cameras")

    def __len__(self) -> int:
        """
        Returns:

            length of internal dict of attributes. (Result of `len(obj)`)
        """
        return len(self._data)

    def __repr__(self) -> str:
        """
        Returns:

            Representation of Manifest. (Result of `repr(obj)`)
        """
        return repr_gen(__class__, self)

    def __str__(self) -> Optional[str]:
        """
        Returns:

            Name of the Rover. (Result of `str(obj)`)
        """
        return self.name

    def __eq__(self, value) -> bool:
        """
        Checks if two objects are same using `rover_id`.

        Returns:

            Result of `obj == obj`.
        """
        return isinstance(value, self.__class__) and value.rover_id == self.rover_id

    def __hash__(self) -> int:
        """
        Returns:

            hash of the class. (Result of `hash(obj)`)
        """
        return hash(self.__class__)

    @property
    def launch_date(self) -> date:
        """
        The Rover's launch date from Earth.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(datetime.strptime(self._data["launch_date"], "%Y-%m-%d"))

    @property
    def landing_date(self) -> date:
        """
        The Rover's landing date on Mars.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(datetime.strptime(self._data["landing_date"], "%Y-%m-%d"))

    @property
    def max_date(self) -> date:
        """
        The most recent Earth date from which photos exist.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(datetime.strptime(self._data["max_date"], "%Y-%m-%d"))

    def search_camera(self, camera: str) -> list:
        """
        Looks for the camera supplied.

        Args:

            camera: The camera to look for. (Must be in Upper case and short name. like: `PANCAM`)

        Returns:

            list of cameras with that name.
        """  # noqa: E501
        camera_data = self.cameras
        if isinstance(camera_data, list):
            try:
                return [cam["name"] for cam in camera_data if camera == camera]
            except KeyError:
                raise BadContentError(content=camera_data) from None
        else:
            raise BadContentError(message=f"can't iterate over <{camera_data}>.")
