## Here are some Frequently Asked Questions.
(Which are not frequently asked ofc)

-----

### <u>Q1</u>) Will there be a sync. release?

<u>Ans</u>) Yes. Sync release will be proposed in v0.6.0 and it won't require
any other dependency since httpx has async and sync support both.

*Added in 0.6.0*.

--------------------

### <u>Q2</u>) Does it support Paginantion?

<u>Ans</u>) Yes. It supports basic Paginantion the API provides.
Marsworks also provides its own paginantion function for
more complicated Paginantion. Which is `helpers.mw_pageit`.

--------------------

### <u>Q3</u>) Is this Wrapper by NASA?

<u>Ans</u>) No. This wrapper is made by me and its mine. As of now at least ;)

--------------------

### <u>Q4</u>) Can i contribute to Marsworks repo?

<u>Ans</u>) Sure!

--------------------

### <u>Q5</u>) Will there be breaking changes in near future?

<u>Ans</u>) Breaking Changes will be proposed until 1.x release but i can say that
they **might not** be any big even in 0.x releases because most of the wrapper is
completed.

--------------------
### <u>Q6</u>) Why can't i use Photo.save() or Photo.read() in coroutine functions?

<u>Ans</u>) You must not use these two methods in a coroutine function because these two are **not**
coroutines and will read or (read and) save the image synchronously. (yeah, they will block.)
Apart from this, due to the wrapper's design, if you ran these in a coro. func. then they will even create
an uncloseable `httpx.Client()` no matter if you have passed `httpx.AsyncClient()` or anything.
Use `await Photo.aread()` and `await Photo.asave()` instead.

### <u>Q7</u>) Why am i getting x error or warning?

------------

#### <u>i</u>) Unclosed `<httpx.AsyncClient object at 0xsome_memory_location>`

Sample:

```py
UserWarning: Unclosed <httpx.AsyncClient object at 0x00000278666EF5B0>. See https://www.python-httpx.org/async/#opening-and-closing-clients for details.
```

<u>Ans</u>) This is because the AsyncClient session which the wrapper is using is not
closed. It is recommended to use `await Client.close()` or use the context manager.

It is recommended to close it only when your purpose for using the session is over. As
AsyncClient session can be reused.


*It can close user given AsyncClient session too.*

---------------

#### <u>ii</u>) UserWarning: Using DEMO_KEY for api call. Please use your api key.

Sample:

```py
UserWarning: Using DEMO_KEY for api call. Please use your api key.
```
<u>Ans</u>) This warning is sent by the wrapper when API call is being made using `DEMO_KEY`
due to some reason. (Mainly because the user has not passed their NASA API key). This can be
solved either by passing your own API-key in `marswork.Client`or by suppressing warnings by
doing `marsworks.Client(suppress_warnings=True)`.

*It is recommended to use your own API key as it has higher X-Ratelimit-Remaining.*

---------------

#### <u>iii</u>) UserWarning: Invalid value was passed for camera. Making request without camera.

Sample:

```py
UserWarning: Invalid value was passed for camera. Making request without camera.
```
<u>Ans</u> This warning is sent when an invalid camera is passed to camera param of a Client method
as stated in the warning. camera only accepts either string name of an enum of [Camera](../API-Reference/Enums/camera/) (not case sensitive) or the enum itself.

*As stated in the warning, the camera param will not be included in the API request if its invalid.*

-----------------

#### <u>iv</u>) ValueError: SOMETHING is not a valid X

Sample:

```py
ValueError: 'XYZ' is not a valid Rover
```
<u>Ans</u>) This error is raised when you have passed an invalid argument to `name` parameter of
a Client method. The arg(s) you have passed were neither an enum of [Rover](../API-Reference/Enums/rover/)
or string name of any enum.

*You can pass an enum itself too like `await Client.get_mission_manifest(Rover.SPIRIT)`.*
