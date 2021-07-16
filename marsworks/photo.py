import inspect
from datetime import datetime, date
from typing import Optional

__all__ = ("Photo",)


class Photo:
    """
    A class representing a Photo.

    Attributes:
        photo_id (int): ID of the photo.
        sol (int): Sol when the photo was taken.
        img_src (str): Image url.
    """

    __slots__ = ("_data", "photo_id", "sol", "_camera", "img_src", "_rover")

    def __init__(self, data: dict):
        self._data: dict = data
        self._camera: dict = data.get("camera", {})
        self._rover: dict = data.get("rover", {})
        self.photo_id: int = data.get("id")
        self.sol: int = data.get("sol")
        self.img_src: str = data.get("img_src")

    def __len__(self) -> int:
        """
        Returns:
            length of internal dict of attributes.
        """
        return len(self._data)

    def __str__(self) -> str:
        """
        Returns:
            url of image.
        """
        return self.img_src

    def __eq__(self, value) -> bool:
        """
        Checks if two objects are same using photo_id.

        Returns:
            result of `o==o`.
        """
        return isinstance(value, self.__class__) and value.photo_id == self.photo_id

    def __hash__(self) -> int:
        """
        Returns:
            hash of the class.
        """
        return hash(self.__class__)

    def __repr__(self) -> str:
        """
        Returns:
            Representation of Photo.
        """
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"

    @property
    def camera_id(self) -> Optional[int]:
        """
        ID of camera with which photo was taken.

        Returns:
            The id as an integer.
        """
        return self._camera.get("id")

    @property
    def camera_name(self) -> Optional[str]:
        """
        Name of camera with which photo was taken.

        Returns:
            The name as a string.
        """
        return self._camera.get("name")

    @property
    def camera_rover_id(self) -> Optional[int]:
        """
        Rover id on which this camera is present.

        Returns:
            The rover id as an integer.
        """
        return self._camera.get("rover_id")

    @property
    def camera_full_name(self) -> Optional[str]:
        """
        Full-Name of camera with which photo was taken.

        Returns:
            The full-name as a string.
        """
        return self._camera.get("full_name")

    @property
    def rover_id(self) -> Optional[int]:
        """
        Similar to `camera_rover_id`.

        Returns:
            The rover id as an integer.
        """
        return self._rover.get("id")

    @property
    def rover_name(self) -> Optional[str]:
        """
        Name of rover which took the photo.

        Returns:
            The name as a string.
        """
        return self._rover.get("name")

    @property
    def rover_landing_date(self) -> Optional[date]:
        """
        The Rover's landing date on Mars.

        Returns:
            An [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._rover.get("landing_date"), "%Y-%m-%d")
        )

    @property
    def rover_launch_date(self) -> Optional[date]:
        """
        The Rover's launch date from Earth.

        Returns:
            An [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._rover.get("launch_date"), "%Y-%m-%d")
        )

    @property
    def rover_status(self) -> Optional[str]:
        """
        The Rover's mission status.

        Returns:
            The rover's mission status as string.
        """
        return self._rover.get("status")
