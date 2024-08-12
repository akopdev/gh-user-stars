import asyncio
import re
from typing import List, Optional

import aiohttp
from pydantic import TypeAdapter

from .schemas import Repository


class Stars:
    def __init__(self, username: str, token: str = None, per_page: int = 10, timeout: int = 60):
        self.token = token
        self.username = username
        self.per_page = per_page
        self.timeout = timeout

    def next_page(self, headers: str) -> Optional[int]:
        links = {}
        for link in headers.split(","):
            result = re.findall(r'<(.*)&page=([0-9]+)>;\s*rel="(\w+)"', link)
            links[result[0][2]] = result[0][1]
        if "next" in links:
            return int(links["next"])

    async def fetch(self, page: int = 1, attempt: int = 1) -> List[Repository]:
        result = []
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.github.com/users/{self.username}/starred",
                headers={"Accept": "application/vnd.github+json"},
                params={"per_page": self.per_page, "page": page},
            ) as response:
                data = await response.json()
                # Check if rate limit exceeded, wait 60 seconds and try again
                if response.status == 403 and attempt < 3:
                    await asyncio.sleep(self.timeout)
                    return await self.fetch(page, attempt + 1)
                try:
                    repositores = TypeAdapter(List[Repository])
                    result.extend(repositores.validate_python(data))
                except Exception:
                    return result
                if next_page := self.next_page(response.headers.get("Link")):
                    result.extend(await self.fetch(next_page))
        return result
