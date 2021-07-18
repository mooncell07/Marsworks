from enum import Enum

__all__ = ("Camera", "Rover")


class Camera(Enum):
    """
    An Enum class.

    | Name      | Value   | Description                                        | Curiosity | Opportunity | Spirit |
    |-----------|---------|----------------------------------------------------|-----------|-------------|--------|
    | `FHAZ`    | FHAZ    | Front Hazard Avoidance Camera                      | ✔         | ✔          | ✔      |
    | `RHAZ`    | RHAZ    | Rear Hazard Avoidance Camera                       | ✔         | ✔          | ✔      |
    | `MAST`    | MAST    | Mast Camera                                        | ✔         |             |        |
    | `CHEMCAM` | CHEMCAM | Chemistry and Camera Complex                       | ✔         |             |        |
    | `MAHLI`   | MAHLI   | Mars Hand Lens Imager                              | ✔         |             |        |
    | `MARDI`   | MARDI   | Mars Descent Imager                                | ✔         |             |        |
    | `NAVCAM`  | NAVCAM  | Navigation Camera                                  | ✔         | ✔           | ✔     |
    | `PANCAM`  | PANCAM  | Panoramic Camera                                   |           | ✔           | ✔      |
    | `MINITES` | MINITES | Miniature Thermal Emission Spectrometer (Mini-TES) |           | ✔           | ✔      |

    """  # noqa: E501

    FHAZ = "FHAZ"
    RHAZ = "RHAZ"
    MAST = "MAST"
    CHEMCAM = "CHEMCAM"
    MAHLI = "MAHLI"
    MARDI = "MARDI"
    NAVCAM = "NAVCAM"
    PANCAM = "PANCAM"
    MINITES = "MINITES"


class Rover(Enum):
    """
    An Enum class.

    | Name          | Value       | Description                                 |
    |---------------|-------------|---------------------------------------------|
    | `CURIOSITY`   | CURIOSITY   | Mars Science Laboratory mission, Curiosity. |
    | `OPPORTUNITY` | OPPORTUNITY | Mars Exploration Rover – B, Opportunity.    |
    | `SPIRIT`      | SPIRIT      | Mars Exploration Rover – A, Spirit.         |

    """

    CURIOSITY = "CURIOSITY"
    OPPORTUNITY = "OPPORTUNITY"
    SPIRIT = "SPIRIT"
    # PERSEVERANCE = "PERSEVERANCE"  >:)
