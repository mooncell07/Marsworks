<img src=https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/pia23378-16.jpg class="center">

<p align="center">
 <img alt="mypy" src="https://github.com/mooncell07/Marsworks/actions/workflows/mypy.yml/badge.svg?event=push" height=28>

 <img alt="PyPI version" src="https://badge.fury.io/py/marsworks.svg" height=28>

<img src="https://img.shields.io/pypi/l/marsworks" height=28>

 <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" height=28>
</p>


# <u>Welcome</u>!

Hi! Welcome to my repository Marsworks! (Name
inspired from fate franchise ofc ;) ).

So, Marsworks is a fast and lightweight API wrapper around
[Mars Rover Photos API](https://api.nasa.gov/) written in Python.

Let's see why you should or shouldn't use this wrapper in next sections.

### <u>Advantages</u>

- Sync & Async support with Async utilizing async-await syntax.
- Fast, lightweight and memory optimized.
- Provides API request handling at really low as
well as high level.
- 100% API coverage.
- Pagination supported.
- Minimal dependency of just 1 for both sync & async support.

### <u>Disadvantages</u>

- No Caching.
- No Ratelimit handling or request quering.
- Not well tested.

*Currently this project is under development and possibilities of
breaking changes in near future is huge until 1.x release.*

----------------

# <u>Getting Started</u>

### <u>Installation</u>

`pip install -U marsworks`

*or*

`python -m pip install -U git+https://github.com/mooncell07/Marsworks.git`

### <u>Usage</u>

#### <u>Async. usage</u>

###### Getting photos on a particular sol taken by this rover, asynchronously.

```py

import asyncio

import marsworks


client = marsworks.AsyncClient()


async def main(rover_name, sol) -> list:
    images = await client.get_photo_by_sol(rover_name, sol)  # You can pass camera too.
    return images


imgs = asyncio.run(main("Curiosity", 956))
print(imgs[0].img_src)
print(imgs[0].photo_id)
# and many more attributes!
```

#### <u>Sync. usage</u>

###### Getting photos on a particular sol taken by this rover, synchronously.

```py

import marsworks


client = marsworks.SyncClient()


def main(rover_name, sol) -> list:
    images = client.get_photo_by_sol(rover_name, sol)  # You can pass camera too.
    return images


imgs = main("Curiosity", 956)
print(imgs[0].img_src)
print(imgs[0].photo_id)
# and many more attributes!
```

------------------

# <u>Links</u>

- #### <u>Marsworks [Github Repo](https://github.com/mooncell07/Marsworks/).</u>

- #### <u>Marsworks PyPi [Page](https://pypi.org/project/marsworks/).</u>

- #### <u>NASA APIs [Page](https://api.nasa.gov/).</u>

- #### <u>Thanks to [Andy](https://github.com/an-dyy) for his contribution.
