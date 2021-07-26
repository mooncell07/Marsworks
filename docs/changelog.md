
# v0.4.0

<u>**Changes:**</u>

*0.3.3*
- `helpers.Page` is now a dataclass.
- `await Serializer.manifest_content()` and `await Serializer.photo_content()`
are no more awaitable.

*0.3.2*:

- Adds `await Client.get_raw_response()`.
- `Serializer` class is now partially public. `await Client.get_raw_response()` returns
this object.
- `Serializer` is now documented.

*0.3.1*:

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
- Adds `BadArgumentError.expected` and `BadArgumentError.got`
- Fixed some typos in docs and fixed examples.
