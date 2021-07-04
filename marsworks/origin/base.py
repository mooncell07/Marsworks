import aiohttp


__all__ = ("Base",)


class Base:

    __slots__ = ("response", "url", "status", "ok", "headers")

    def __init__(self, response: aiohttp.ClientResponse) -> None:
        self.response: aiohttp.ClientSession = response
        self.url: str = response.url
        self.status: int = response.status
        self.ok: bool = response.ok
        self.headers: dict = response.headers

    async def content(self) -> dict:
        return await self.response.json()
