from marsworks.origin.exceptions import BadContentError
import typing
from datetime import datetime

__all__ = ("Manifest",)


class Manifest:

    __slots__ = (
        "_data",
        "rover_id",
        "name",
        "status",
        "max_sol",
        "total_photos",
        "cameras",
        "__properties",
    )

    def __init__(self, data: dict):
        self._data: dict = data
        self.rover_id: int = data.get("id")
        self.name: str = data.get("name")
        self.status: str = data.get("status")
        self.max_sol: int = data.get("max_sol")
        self.total_photos: int = data.get("total_photos")
        self.cameras: dict = data.get("cameras")
        self.__properties: tuple = ("launch_date", "landing_date", "max_date")

    @property
    def launch_date(self) -> datetime.date:
        return datetime.date(
            datetime.strptime(self._data.get("launch_date"), "%Y-%m-%d")
        )

    @property
    def landing_date(self) -> datetime.date:
        return datetime.date(
            datetime.strptime(self._data.get("landing_date"), "%Y-%m-%d")
        )

    @property
    def max_date(self) -> datetime.date:
        return datetime.date(datetime.strptime(self._data.get("max_date"), "%Y-%m-%d"))

    def search_camera(self, name: str) -> typing.Union[dict, None]:
        camdata = self.cameras
        if isinstance(camdata, typing.Iterable):
            for cam in camdata:
                try:
                    if (
                        cam["name"].lower() == name.lower()
                        or cam["full_name"].lower() == name.lower()
                    ):
                        return cam
                    else:
                        return None
                except KeyError:
                    raise BadContentError(content=camdata) from None
        else:
            raise BadContentError(message=f"can't iterate over <{camdata}>.")

    def __repr__(self):
        form = ""
        slots = self.__class__.__slots__
        items = {
            s: getattr(self, s)
            for s in slots + self.__properties
            if not s.startswith("_")
        }
        for i in items:
            form += f"{i} = {items[i]}, "
        return f"{self.__class__.__name__}({form})"
