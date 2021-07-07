from marsworks.origin.exceptions import BadContentError
from datetime import datetime
import inspect

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
    )

    def __init__(self, data: dict):
        self._data: dict = data
        self.rover_id: int = data.get("id")
        self.name: str = data.get("name")
        self.status: str = data.get("status")
        self.max_sol: int = data.get("max_sol")
        self.total_photos: int = data.get("total_photos")
        self.cameras: dict = data.get("cameras")

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

    def search_camera(self, ename: str) -> list:
        camdata = self.cameras
        if isinstance(camdata, list):
            try:
                fcam = filter(lambda c: c["name"] == ename.name, camdata)
                return list(fcam)
            except KeyError:
                raise BadContentError(content=camdata) from None
        else:
            raise BadContentError(message=f"can't iterate over <{camdata}>.")

    def __repr__(self):
        form = ""
        items = filter(lambda a: not a[0].startswith("_"), inspect.getmembers(self))

        for i in items:
            form += f"{i[0]} = {i[1]}, "
        return f"{self.__class__.__name__}({form[:-2]})"
