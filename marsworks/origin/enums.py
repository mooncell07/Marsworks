from enum import Enum, auto

__all__ = ("Camera", "Rover")


class Camera(Enum):
    FHAZ = auto()
    RHAZ = auto()
    MAST = auto()
    CHEMCAM = auto()
    MAHLI = auto()
    MARDI = auto()
    NAVCAM = auto()
    PANCAM = auto()
    MINITES = auto()


class Rover(Enum):
    Spirit = auto()
    Opportunity = auto()
    Curiosity = auto()
    # Perseverance = auto() >:)
