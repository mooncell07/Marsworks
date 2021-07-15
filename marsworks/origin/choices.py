__all__ = ("Camera", "Rover")


class Camera:
    """
    Attributes:
        FHAZ (str): Front Hazard Avoidance Camera
        RHAZ (str): Rear Hazard Avoidance Camera
        MAST (str):	Mast Camera
        CHEMCAM (str): Chemistry and Camera Complex
        MAHLI (str): Mars Hand Lens Imager
        MARDI (str): Mars Descent Imager
        NAVCAM (str): Navigation Camera
        PANCAM (str): Panoramic Camera
        MINITES (str): Miniature Thermal Emission Spectrometer (Mini-TES)

    Note:
        All above mentioned attributes are class attributes.

    Note:
        This class is an iterable.
    """

    FHAZ = "FHAZ"
    RHAZ = "RHAZ"
    MAST = "MAST"
    CHEMCAM = "CHEMCAM"
    MAHLI = "MAHLI"
    MARDI = "MARDI"
    NAVCAM = "NAVCAM"
    PANCAM = "PANCAM"
    MINITES = "MINITES"

    def __iter__(self):
        return iter([i for i in vars(__class__) if not i.startswith("_")])


class Rover:
    """
    Attributes:
        CURIOSITY (str): Mars Science Laboratory mission, Curiosity.
        OPPORTUNITY (str): Mars Exploration Rover – B, Opportunity.
        SPIRIT (str): Mars Exploration Rover – A, Spirit.

    Note:
        All above mentioned attributes are class attributes.

    Note:
        This class is an iterable.
    """

    CURIOSITY = "CURIOSITY"
    OPPORTUNITY = "OPPORTUNITY"
    SPIRIT = "SPIRIT"
    # PERSEVERANCE = "PERSEVERANCE"  >:)

    def __iter__(self):
        return iter([i for i in vars(__class__) if not i.startswith("_")])
