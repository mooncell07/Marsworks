import aiohttp
import typing

__all__ = (
    "MarsworksError",
    "BadStatusCodeError",
    "ContentTypeError",
    "BadContentError",
)


class MarsworksError(Exception):
    __slots__ = ()
    ...


class BadStatusCodeError(MarsworksError):

    __slots__ = ("reason", "status")

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.reason = response.reason
        self.status = response.status
        super().__init__(
            f"Encountered Bad status code of <{self.status} {self.reason}> "
            f"from the API."
        )


class ContentTypeError(MarsworksError):

    __slots__ = ("content_type",)

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.content_type = response.content_type
        super().__init__(f"Expected <application/json> got <{self.content_type}>.")


class BadContentError(MarsworksError):

    __slots__ = ("content",)

    def __init__(self, *, content: typing.Any = None, message: str = None) -> None:
        self.content = content
        self.message = (
            f"Recieved malformed/bad content <{content}>." if not message else message
        )

        super().__init__(self.message)
