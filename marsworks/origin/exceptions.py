import aiohttp
import typing

__all__ = (
    "MarsworksError",
    "BadStatusCodeError",
    "ContentTypeError",
    "BadContentError",
    "BadArgumentError",
)


class MarsworksError(Exception):

    __slots__ = ("headers",)

    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(self.error)


class BadStatusCodeError(MarsworksError):

    __slots__ = ("reason", "status")

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.reason = response.reason
        self.status = response.status
        if self.status != 429:
            super().__init__(
                f"Encountered Bad status code of <{self.status} {self.reason}> "
                f"from the API."
            )
        else:
            super().__init__("We are being Ratelimited!")


class ContentTypeError(MarsworksError):

    __slots__ = ("content_type",)

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.content_type = response.content_type
        super().__init__(
            f"Expected <application/json> or <image/jpeg> got <{self.content_type}>."
        )


class BadContentError(MarsworksError):

    __slots__ = ("content",)

    def __init__(self, *, content: typing.Any = None, message: str = None) -> None:
        self.content = content
        self.message = (
            f"Recieved malformed/bad content <{content}>." if not message else message
        )

        super().__init__(self.message)


class BadArgumentError(MarsworksError):
    ...
