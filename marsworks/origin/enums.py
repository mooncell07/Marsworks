from enum import Enum, auto

__all__ = ("Cameras", "RoverName")


class Cameras(Enum):
    FHAZ = auto()
    RHAZ = auto()
    MAST = auto()
    CHEMCAM = auto()
    MAHLI = auto()
    MARDI = auto()
    NAVCAM = auto()
    PANCAM = auto()
    MINITES = auto()


class RoverName(Enum):
    Spirit = auto()
    Opportunity = auto()
    Curiosity = auto()
    # Perseverance = auto() >:)
