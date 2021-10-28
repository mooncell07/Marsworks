# v0.7.0

<u>**Changes:**</u>

- `marsworks.Client` renamed to `marsworks.AsyncClient`.
- `marsworks.AlterClient` renamed to `marsworks.SyncClient`.
- Removed `AsyncClient.save()` and `AsyncClient.read()`.
- Fixed Typehints.
- Removed `Manifest.__hash__()` and `Photo.__hash__()`.
- Removed `Manifest.search_camera()`.
- Fixed `Photo.read()`, `Photo.save()`, `Photo.aread()`, `Photo.asave()`.

------------

# v0.6.3

<u>**Changes:**</u>

- Fixed README on PYPI.

------------


# v0.6.1

- No changes. (I had to delete v0.6.0 from PyPi due to some reason)

-----------


# v0.6.0

*Not available, install 0.6.1 instead.*

<u>**Changes:**</u>

*0.5.3*

- Adds `__len__` dunder to `Manifest`.
- Adds some warnings in docs and new question to FAQ.

*0.5.2*

- Rewrites README and docs. landing page.
- Adds `Photo.read()` and `Photo.save()`.
- `AlterClient` is now documented.
- Adds `AlterClient.get_raw_response()`.

*0.5.1*

- `Client` now has an alias: `AsyncClient`.
- Fixes `TypeError` bug in`await Client.get_photo_by_earthdate()` and
`await Client.get_latest_photo()`.
- Adds `AlterClient.get_mission_status()`, `AlterClient.get_photo_by_sol()`,
`AlterClient.get_photo_by_earthdate()`, `AlterClient.get_latest_photo()`,
`AlterClient.close()`.
- Adds `AlterClient` (alias: `SyncClient`) for synchronous HTTP requesting.

------------

# v0.5.0

<u>**Changes:**</u>

*0.4.3*

- `rover_name`, `status`, `rover_id`, `rover_landing_date`, `rover_launch_date`
are moved from `Photo` to `PartialManifest`.
- Added `rover` property to `Photo`. It returns `PartialManifest`.
- Adds `PartialManifest` class.
- Now all public `repr`s of marsworks have attribute value represented as well.

*0.4.2*

- Beautifies docstrings for hint bubble in many text editors.
- Fixes `Serializer.photo_content()`. Now it doesn't return empty list.

*0.4.1*

- `helpers.lookup()` now returns first element which meets the predicate. Use
`filter()` to achieve what it could do before.
- Fixed some typehints and docstrings.
- Adds `await Photo.read()` and `await Photo.save()`.
- Deprecates `await Client.read()` and `await Client.save()`.
- Deprecates `BadArgumentError`.

---------------

# v0.4.0

<u>**Changes:**</u>

*0.3.4*

- Adds FAQ page in Documentation.
- All Client methods which accept `camera` param can now send `UserWarning` when an invalid `camera` is
passed. They can be suppressed with `marsworks.Client(suppress_warnings=True)`.
- `await Client.save()` and `await Client.read()` are now Pending Deprecated. They will be Deprecated in
0.5.0 and removed in 1.0.0. The replacement will be proposed in 0.5.0.

*0.3.3*

- `helpers.Page` is now a dataclass.
- `Serializer.manifest_content()` and `Serializer.photo_content()`.
are no more awaitable.
- `BadContentError` Can be raised in `Serializer.photo_content(...)`.

*0.3.2*

- Adds `await Client.get_raw_response()`.
- `Serializer` class is now partially public. `await Client.get_raw_response()` returns
this object.
- `Serializer` is now documented.

*0.3.1*

- Adds `Rover.perseverance` and all the Camera enums of Perseverance. There are too many so
haven't listed here.
- Adds `helper` module, this module has some helper methods to help in working with data. Currently
`helper.lookup()` and `helper.mw_pageit()` are only added.

---------------

# v0.3.0

<u>**Changes:**</u>

- Adds `await Client.get_latest_photo()` and `Photo.parse_img_src()`.
- `choices` is now `enums`.
- Now all `await Client.get_x` take a `page` argument.
- Now python 3.7 and above are supported.
- Now `await Client.get_photo_by_earthdate()`'s `earth_date` param takes either `datetime.date` object
or string in `YYYY-MM-DD` form.
- Exceptions are now documented.
- Adds `BadArgumentError.expected` and `BadArgumentError.got`.
- Fixed some typos in docs and fixed examples.
