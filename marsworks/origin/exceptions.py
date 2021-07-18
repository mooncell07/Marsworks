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

    Attributes:
        error (str): The error message.
    """

    __slots__ = ("headers",)

    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(self.error)


class BadStatusCodeError(MarsworksError):
    """
    Raised when a bad status code is recieved.

    Attributes:
        reason (str): The reason phrase of status.
        status (int): The status code of response.
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
    Raised when content recieved is neither application/json nor image/jpeg.

    Attributes:
        content_type (str): The content type API returned.
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
    Raised when API returns bad or malformed content.
    """

    __slots__ = ("content",)

    def __init__(self, *, content: typing.Any = None, message: str = None) -> None:
        self.__content = content
        self.__message = (
            f"Recieved malformed/bad content <{content}>." if not message else message
        )

        super().__init__(self.__message)


class BadArgumentError(MarsworksError):
    """
    Raised when bad values are supplied to any method.

    Attributes:
        expected (str): The type of arg this method expected.
        got (str): The type of arg this method got.
    """

    __slots__ = ("expected", "got")

    def __init__(self, expected: str, got: str):
        self.expected = expected
        self.got = got

        super().__init__(
            f"Expected arg of type {self.expected} " f"but got {self.got}."
        )
