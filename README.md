<img src=https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia23378-16.jpg class="center">

<p align="center">
 <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</p>


# Welcome!
Marsworks is an Async. Python API Wrapper around NASA's
[Mars Rover Photos API](https://api.nasa.gov/) with 100% API coverage.

Currently this project is under development and possibilities of
breaking changes in near future is huge until 1.x release.

# Getting Started

## Installation:

NotImplemented

## Usage:

```py

#Lets get images using sols.
import asyncio
from marsworks import Client, Rover

client = Client()
async def main(rover_name, sol) -> list:
    print(await client.get_photo_by_sol(rover_name, sol)) #You can pass camera too.


asyncio.run(main(Rover.Curiosity, 956))
#We now have all the photo urls and info
# in form of list of Photo objects on 956th sol.
```

```py

#Lets get some mission manifest.
import asyncio
from marsworks import Client, Manifest, Rover

client = Client()
async def main(rover_name) -> Manifest:
    return await client.get_mission_manifest(rover_name)

mfst = asyncio.run(main(Rover.Spirit))
print(mfst.landing_date)
print(mfst.status)
#and more!
```

# Docs. can be found [here](https://novaemiya.github.io/Marsworks/)!
