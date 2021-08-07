from datetime import date, datetime
from typing import Optional

from .origin.internal_utils import repr_gen

__all__ = ("PartialManifest",)


class PartialManifest:
    """
    A class representing a `PartialManifest`.

    Attributes:

        rover_name (str): Name of rover which took the photo.
        status (str): The Rover's mission status.
        rover_id (int): The Rover's id.
    """

    def __init__(self, rover_info: dict = {}):
        self._rover_info: dict = rover_info
        self.rover_name: str = rover_info.get("name")
        self.status: str = rover_info.get("status")
        self.rover_id: int = rover_info.get("id")

    @property
    def rover_landing_date(self) -> Optional[date]:
        """
        The Rover's landing date on Mars.

        Returns:

            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._rover_info["landing_date"], "%Y-%m-%d")
        )

    @property
    def rover_launch_date(self) -> Optional[date]:
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

        return repr_gen(__class__, self)

    def __hash__(self) -> int:
        """
        Returns:

            hash of the class. (Result of `hash(obj)`)
        """
        return hash(self.__class__)

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

    def __str__(self) -> Optional[str]:
        """
        Returns:

            Name of the rover. (Result of `str(obj)`)
        """
        return self.rover_name
