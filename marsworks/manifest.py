import inspect
from datetime import datetime

from marsworks.origin.decors import ensure_type
from marsworks.origin.exceptions import BadContentError

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

    def __init__(self, data: dict) -> None:
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

    @ensure_type
    def search_camera(self, camera: str) -> list:
        camdata = self.cameras
        if isinstance(camdata, list):
            try:
                fcam = filter(lambda c: c["name"] == camera.name, camdata)
                return list(fcam)
            except KeyError:
                raise BadContentError(content=camdata) from None
        else:
            raise BadContentError(message=f"can't iterate over <{camdata}>.")

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"
