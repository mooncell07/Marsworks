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

    - Perseverance Cameras

    | Name                   | Value                | Description                           |
    |------------------------|----------------------|---------------------------------------|
    | `EDL_RUCAM`            | EDL_RUCAM            | Rover-UpLook Camera                   |
    | `EDL_RDCAM`            | EDL_RDCAM            | Rover Down-Look Camera                |
    | `EDL_DDCAM`            | EDL_DDCAM            | Descent Stage Down-Look Camera        |
    | `EDL_PUCAM1`           | EDL_PUCAM1           | Parachute Up-Look Camera A            |
    | `EDL_PUCAM2`           | EDL_PUCAM2           | Parachute Up-Look Camera B            |
    | `NAVCAM_LEFT`          | NAVCAM_LEFT          | Navigation Camera - Left              |
    | `NAVCAM_RIGHT`         | NAVCAM_RIGHT         | Navigation Camera - Right             |
    | `MCZ_RIGHT`            | MCZ_RIGHT            | Mast Camera Zoom - Right              |
    | `MCZ_LEFT`             | MCZ_LEFT             | Mast Camera Zoom - Left               |
    | `FRONT_HAZCAM_LEFT_A`  | FRONT_HAZCAM_LEFT_A  | Front Hazard Avoidance Camera - Left  |
    | `FRONT_HAZCAM_RIGHT_A` | FRONT_HAZCAM_RIGHT_A | Front Hazard Avoidance Camera - Right |
    | `REAR_HAZCAM_LEFT`     | REAR_HAZCAM_LEFT     | Rear Hazard Avoidance Camera - Left   |
    | `REAR_HAZCAM_RIGHT`    | REAR_HAZCAM_RIGHT    | Rear Hazard Avoidance Camera - Right  |
    | `SKYCAM`               | SKYCAM               | MEDA Skycam                           |
    | `SHERLOC_WATSON`       | SHERLOC_WATSON       | SHERLOC WATSON Camera                 |
    | `SUPERCAM_RMI`         | SUPERCAM_RMI         | SuperCam Remote Micro Imager          |
    | `LCAM`                 | LCAM                 | Lander Vision System Camera           |

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

    EDL_RUCAM = "EDL_RUCAM"
    EDL_RDCAM = "EDL_RDCAM"
    EDL_DDCAM = "EDL_DDCAM"
    EDL_PUCAM1 = "EDL_PUCAM1"
    EDL_PUCAM2 = "EDL_PUCAM2"
    NAVCAM_LEFT = "NAVCAM_LEFT"
    NAVCAM_RIGHT = "NAVCAM_RIGHT"
    MCZ_RIGHT = "MCZ_RIGHT"
    MCZ_LEFT = "MCZ_LEFT"
    FRONT_HAZCAM_LEFT_A = "FRONT_HAZCAM_LEFT_A"
    FRONT_HAZCAM_RIGHT_A = "FRONT_HAZCAM_RIGHT_A"
    REAR_HAZCAM_LEFT = "REAR_HAZCAM_LEFT"
    REAR_HAZCAM_RIGHT = "REAR_HAZCAM_RIGHT"
    SKYCAM = "SKYCAM"
    SHERLOC_WATSON = "SHERLOC_WATSON"
    SUPERCAM_RMI = "SUPERCAM_RMI"
    LCAM = "LCAM"


class Rover(Enum):
    """
    An Enum class.

    | Name           | Value        | Description                                 |
    |----------------|--------------|---------------------------------------------|
    | `CURIOSITY`    | CURIOSITY    | Mars Science Laboratory mission, Curiosity. |
    | `OPPORTUNITY`  | OPPORTUNITY  | Mars Exploration Rover – B, Opportunity.    |
    | `SPIRIT`       | SPIRIT       | Mars Exploration Rover – A, Spirit.         |
    | `PERSEVERANCE` | PERSEVERANCE | Mars 2020 Rover, Perseverance.              |

    """

    CURIOSITY = "CURIOSITY"
    OPPORTUNITY = "OPPORTUNITY"
    SPIRIT = "SPIRIT"
    PERSEVERANCE = "PERSEVERANCE"
