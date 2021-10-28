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

from datetime import date, datetime
from typing import Optional, Mapping, Any

from .partialmanifest import PartialManifest

__all__ = ("Manifest",)


class Manifest(PartialManifest):
    """
    A class representing a `Manifest`.

    Attributes:

        rover_id (Optional[int]): ID of the rover.
        rover_name (str): Name of the Rover.
        status (Optional[str]): The Rover's mission status.
        max_sol (Optional[int]): The most recent Martian sol from which photos exist.
        total_photos (Optiona[int]): Number of photos taken by that Rover.
        cameras (Mapping[str, str]): Cameras for which there are photos by that Rover on that sol.
    """  # noqa: E501

    __slots__ = (
        "max_sol",
        "total_photos",
        "cameras",
    )

    def __init__(self, data: Mapping[Any, Any]) -> None:
        super().__init__(data)
        self.max_sol: Optional[int] = data.get("max_sol")
        self.total_photos: Optional[int] = data.get("total_photos")
        self.cameras: Mapping[str, str] = data.get("cameras", {})

    def __eq__(self, value: Any) -> bool:
        """
        Checks if two objects are same using `rover_id`.

        Returns:

            Result of `obj == obj`.
        """
        return isinstance(value, self.__class__) and value.rover_id == self.rover_id

    @property
    def max_date(self) -> date:
        """
        The most recent Earth date from which photos exist.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._rover_info["max_date"], "%Y-%m-%d")
        )
