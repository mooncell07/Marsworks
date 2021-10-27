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

import inspect
import warnings
from typing import Optional, Union, Any


from .enums import Camera

__all__ = (
    "repr_gen",
    "validate_cam",
)


def repr_gen(obj: Any) -> str:
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
    return f"{obj.__class__.__name__}({fmt})"


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
