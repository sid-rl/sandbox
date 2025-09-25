import asyncio
import os
from runloop_api_client import AsyncRunloop

client = AsyncRunloop(bearer_token=os.environ.get("RUNLOOP_API_KEY"))

async def shutdown_devboxes():
    devboxes = await client.devboxes.list(status="running")
    for devbox in devboxes.devboxes:
        await client.devboxes.shutdown(devbox.id)

asyncio.run(shutdown_devboxes())