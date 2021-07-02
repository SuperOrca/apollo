from io import BytesIO

from httpx import AsyncClient, Response


async def geturljson(url) -> dict:
    async with AsyncClient() as client:
        data = await client.get(url)
        return data.json()


async def geturlbytes(url) -> BytesIO:
    async with AsyncClient() as client:
        data = await client.get(url)
        return BytesIO(data.read())


async def geturl(url) -> Response:
    async with AsyncClient() as client:
        return await client.get(url)
