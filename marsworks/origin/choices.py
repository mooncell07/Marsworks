__all__ = ("Camera", "Rover")


class Camera:
    """
    All available Camera options.
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
    All available Rover options.
    """

    SPIRIT = "Spirit"
    OPPORTUNITY = "Opportunity"
    CURIOSITY = "Curiosity"
    # PERSEVERANCE = "Perseverance"  >:)

    def __iter__(self):
        return iter([i for i in vars(__class__) if not i.startswith("_")])
