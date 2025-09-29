import os
import asyncio
from runloop_api_client import AsyncRunloop

client = AsyncRunloop(base_url=os.environ.get("RUNLOOP_BASE_URL"))

async def main():
    scenario_run_id = "scr_3194MkkpGpVpqsgnEcknj"
    result = await client.scenarios.runs.score_and_await(scenario_run_id)
    print(result)

asyncio.run(main())