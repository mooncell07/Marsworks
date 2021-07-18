# v0.3.0

**Changes**:

- Adds `await Client.get_latest_photo()` and `Photo.parse_img_src()`.
- `choices` is now `enums`.
- Now all `await Client.get_x` take a `page` argument.
- Now python 3.7 and above are supported.
- Now `await Client.get_photo_by_earthdate()`'s `earth_date` param takes either `datetime.date` object
or string in `YYYY-MM-DD` form.
- Exceptions are now docummented.
- Adds `BadArgumentError.expected` and `BadArgumentError.got`
- Fixed some typos in docs and fixed examples.
