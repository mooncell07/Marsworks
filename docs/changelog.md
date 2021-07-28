
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
- `Serializer.manifest_content()` and `Serializer.photo_content()`
are no more awaitable.
- `BadContentError` Can be raised in `Serializer.photo_content(...)`

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
