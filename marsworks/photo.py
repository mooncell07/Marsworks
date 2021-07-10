import inspect
from datetime import datetime

__all__ = ("Photo",)


class Photo:

    __slots__ = ("_data", "photo_id", "sol", "_camera", "img_src", "_rover")

    def __init__(self, data: dict):
        self._data: dict = data
        self._camera: dict = data.get("camera")
        self._rover: dict = data.get("rover")
        self.photo_id: int = data.get("id")
        self.sol: int = data.get("sol")
        self.img_src: str = data.get("img_src")

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return self.img_src

    def __eq__(self, value):
        return isinstance(value, self.__class__) and value.photo_id == self.photo_id

    def __hash__(self):
        return hash(self.__class__)

    def __repr__(self):
        fil = filter(
            lambda attr: not attr[0].startswith("_")
            and not callable(getattr(self, attr[0], None)),
            inspect.getmembers(self),
        )
        rpr = "".join(f"{i[0]} = {i[1]}, " for i in fil)[:-2]
        return f"{__class__.__name__}({rpr})"

    @property
    def camera_id(self) -> int:
        return self._camera.get("id")

    @property
    def camera_name(self) -> str:
        return self._camera.get("name")

    @property
    def camera_rover_id(self) -> int:
        return self._camera.get("rover_id")

    @property
    def camera_full_name(self) -> str:
        return self._camera.get("full_name")

    @property
    def rover_id(self) -> int:
        return self._rover.get("id")

    @property
    def rover_name(self) -> str:
        return self._rover.get("name")

    @property
    def rover_landing_date(self) -> datetime.date:
        return datetime.date(
            datetime.strptime(self._rover.get("landing_date"), "%Y-%m-%d")
        )

    @property
    def rover_launch_date(self) -> datetime.date:
        return datetime.date(
            datetime.strptime(self._rover.get("launch_date"), "%Y-%m-%d")
        )

    @property
    def rover_status(self) -> str:
        return self._rover.get("status")
