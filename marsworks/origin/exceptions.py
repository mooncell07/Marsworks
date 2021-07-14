import typing

import httpx

__all__ = (
    "MarsworksError",
    "BadStatusCodeError",
    "ContentTypeError",
    "BadContentError",
    "BadArgumentError",
)


class MarsworksError(Exception):
    """
    Base class for all marsworks exceptions.
    """

    __slots__ = ("headers",)

    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(self.error)


class BadStatusCodeError(MarsworksError):
    """
    Raised when a bad status code is recieved.
    """

    __slots__ = ("reason", "status")

    def __init__(self, response: httpx.Response) -> None:
        self.reason = response.reason_phrase
        self.status = response.status_code
        if self.status != 429:
            super().__init__(
                f"Encountered Bad status code of <{self.status} "
                f"{self.reason}> from the API."
            )
        else:
            super().__init__("We are being Ratelimited!")


class ContentTypeError(MarsworksError):
    """
    Raised when content recieved is neither application/json or image/jpeg.
    """

    __slots__ = ("content_type",)

    def __init__(self, response: httpx.Response) -> None:
        self.content_type = response.headers["content-type"]
        super().__init__(
            "Expected <application/json; charset=utf-8> or "
            f"<image/jpeg> got <{self.content_type}>."
        )


class BadContentError(MarsworksError):
    """
    Unlike `ContentTypeError`, this is raised when content has some fault.
    """

    __slots__ = ("content",)

    def __init__(self, *, content: typing.Any = None, message: str = None) -> None:
        self.content = content
        self.message = (
            f"Recieved malformed/bad content <{content}>." if not message else message
        )

        super().__init__(self.message)


class BadArgumentError(MarsworksError):
    """
    Bad Args are passed to the func.
    """

    ...
