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

`pip install -U marsworks`

## Usage:

```py

#Lets get images using sols.
import asyncio
from marsworks import Client

client = Client()
async def main(rover_name, sol) -> list:
    images = await client.get_photo_by_sol(rover_name, sol) #You can pass camera too.
    return images


imgs = asyncio.run(main("Curiosity", 956))
print(imgs[0].img_src)
print(imgs[0].photo_id)
#and many more!
```

```py

#Lets get some mission manifest.
import asyncio
from marsworks import Client, Manifest

client = Client()
async def main(rover_name) -> Manifest:
    mfest = await client.get_mission_manifest(rover_name)
    return mfest

mfst = asyncio.run(main("Spirit"))
print(mfst.landing_date)
print(mfst.status)
#and more!
```
