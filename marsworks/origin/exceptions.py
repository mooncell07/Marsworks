import aiohttp

__all__ = ("MarsworksError", "BadStatusCodeError", "ContentTypeError")


class MarsworksError(Exception):
    __slots__ = ()
    ...


class BadStatusCodeError(MarsworksError):

    __slots__ = ("reason", "status", "url")

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.reason = response.reason
        self.status = response.status
        self.url = response.url
        super().__init__(
            f"Encountered Bad status code of <{self.status} {self.reason}> "
            f"from {self.url}"
        )


class ContentTypeError(MarsworksError):

    __slots__ = "content_type"

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.content_type = response.content_type
        super().__init__(f"Expected <application/json> got <{self.content_type}>")
