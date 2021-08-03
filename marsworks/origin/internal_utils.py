import inspect
import warnings
from typing import Optional, Union


from .enums import Camera

__all__ = (
    "repr_gen",
    "validate_cam",
)


def repr_gen(cls, obj) -> str:
    """
    Forms a repr for obj.
    """
    attrs = [
        attr
        for attr in inspect.getmembers(obj)
        if not inspect.ismethod(attr[1])
        if not attr[0].startswith("_")
    ]
    fmt = ", ".join(f"{attr}={repr(value)}" for attr, value in attrs)
    return f"{cls.__name__}({fmt})"


def validate_cam(
    sprswrngs: bool, camera: Optional[Union[Camera, str]] = None
) -> Optional[Camera]:
    """
    Validates the camera input.
    """
    if camera is not None:
        try:
            camera = Camera(camera.upper() if isinstance(camera, str) else camera).value
        except ValueError:
            if not sprswrngs:
                warnings.warn(
                    "Invalid value was passed for camera. "
                    "Making request without camera."
                )
            camera = None
    return camera
