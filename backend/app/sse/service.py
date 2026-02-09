import asyncio
from collections import defaultdict


class SSEService:
    def __init__(self):
        self._connections: dict[int, list[asyncio.Queue]] = defaultdict(list)

    def connect(self, store_id: int) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._connections[store_id].append(queue)
        return queue

    def disconnect(self, store_id: int, queue: asyncio.Queue) -> None:
        if queue in self._connections[store_id]:
            self._connections[store_id].remove(queue)

    async def broadcast(self, store_id: int, event: str, data: dict) -> None:
        for queue in self._connections[store_id]:
            await queue.put({"event": event, "data": data})


sse_service = SSEService()
