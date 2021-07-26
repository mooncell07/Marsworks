import inspect
from datetime import datetime, date

from marsworks.origin.exceptions import BadContentError

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
        self.rover_id: int = data.get("id")
        self.name: str = data.get("name")
        self.status: str = data.get("status")
        self.max_sol: int = data.get("max_sol")
        self.total_photos: int = data.get("total_photos")
        self.cameras: dict = data.get("cameras")

    def __repr__(self) -> str:
        """
        Returns:
            Representation of Manifest. (Result of `repr(obj)`)
        """
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"

    def __len__(self) -> int:
        """
        Returns:
            length of internal dict of attributes. (Result of `len(obj)`)
        """
        return len(self._data)

    def __eq__(self, value) -> bool:
        """
        Checks if two objects are same using `rover_id`.

        Returns:
            Result of `obj == obj`.
        """
        return isinstance(value, self.__class__) and value.rover == self.rover_id

    def __str__(self) -> str:
        """
        Returns:
            Name of the Rover. (Result of `str(obj)`)
        """
        return self.name

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
        return datetime.date(
            datetime.strptime(self._data.get("launch_date"), "%Y-%m-%d")
        )

    @property
    def landing_date(self) -> date:
        """
        The Rover's landing date on Mars.

        Returns:
            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(
            datetime.strptime(self._data.get("landing_date"), "%Y-%m-%d")
        )

    @property
    def max_date(self) -> date:
        """
        The most recent Earth date from which photos exist.

        Returns:
            A [datetime.date](https://docs.python.org/3/library/datetime.html?highlight=datetime%20date#datetime.date) object.
        """  # noqa: E501
        return datetime.date(datetime.strptime(self._data.get("max_date"), "%Y-%m-%d"))

    def search_camera(self, camera: str) -> list:
        """
        Looks for the camera supplied.

        Args:
            camera: The camera to look for. (Must be in Upper case and short name. like: `PANCAM`)

        Returns:
            list of cameras with that name.
        """  # noqa: E501
        camdata = self.cameras
        if isinstance(camdata, list):
            try:
                fcam = filter(lambda c: c["name"] == camera, camdata)
                return list(fcam)
            except KeyError:
                raise BadContentError(content=camdata) from None
        else:
            raise BadContentError(message=f"can't iterate over <{camdata}>.")
