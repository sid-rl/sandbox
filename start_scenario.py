import os
import asyncio
from runloop_api_client import AsyncRunloop

client = AsyncRunloop(base_url=os.environ.get("RUNLOOP_BASE_URL"))

async def main():
    scenario_id = "scn_314ZxtW9kizn6qJguIXRS"
    scenario = await client.scenarios.retrieve(scenario_id)
    '''scenario_run = await client.scenarios.start_run_and_await_env_ready(
        scenario_id=scenario_id,
        run_name="test run",
    )'''
    print(scenario.input_context.problem_statement)

asyncio.run(main())