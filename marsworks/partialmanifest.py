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

from datetime import date, datetime
from typing import Optional, Mapping, Any

from .origin.tools import repr_gen

__all__ = ("PartialManifest",)


class PartialManifest:
    """
    A class representing a `PartialManifest`.

    Attributes:

        rover_name (str): Name of rover which took the photo.
        status (str): The Rover's mission status.
        rover_id (int): The Rover's id.
    """

    def __init__(self, rover_info: Mapping[Any, Any] = {}):
        self._rover_info = rover_info
        self.rover_name = rover_info.get("name")
        self.status = rover_info.get("status")
        self.rover_id = rover_info.get("id")

    @property
    def landing_date(self) -> Optional[date]:
        """
        The Rover's landing date on Mars.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._rover_info["landing_date"], "%Y-%m-%d")
        )

    @property
    def launch_date(self) -> Optional[date]:
        """
        The Rover's launch date from Earth.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._rover_info["launch_date"], "%Y-%m-%d")
        )

    def __repr__(self) -> str:
        """
        Returns:

            Representation of Photo. (Result of `repr(obj)`)
        """

        return repr_gen(self)

    def __eq__(self, value) -> bool:
        """
        Checks if two objects are same using `rover_id`.

        Returns:

            Result of `obj == obj`.
        """
        return isinstance(value, self.__class__) and value.rover_id == self.rover_id

    def __len__(self) -> int:
        """
        Returns:

            length of internal dict of attributes. (Result of `len(obj)`)
        """
        return len(self._rover_info)

    def __str__(self) -> str:
        """
        Returns:

            Name of the rover. (Result of `str(obj)`)
        """
        return self.rover_name  # type: ignore
