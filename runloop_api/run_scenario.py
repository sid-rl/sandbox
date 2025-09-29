import os
import asyncio
from runloop_api_client import AsyncRunloop
from shlex import quote

# Note: We are using the AsyncRunloop client throughout the rest of this example.
client = AsyncRunloop(base_url=os.environ.get("RUNLOOP_BASE_URL"))

async def main():
    # page = await client.benchmarks.list_public()
    # benchmarks = page.benchmarks
    # The Benchmark definition contains a list of all scenarios contained in the benchmark
    # print(benchmarks[0].scenario_ids)

    # Note: we are using the async client here.
    scenario_id = "scn_2zmy3xQDpCO6UwQ5WZYx1"
    scenario = await client.scenarios.retrieve(scenario_id)
    scenario_run = await client.scenarios.start_run_and_await_env_ready(
        scenario_id=scenario_id,
        run_name="scikit-learn__scikit-learn-13496 mini-swe-agent test run",
    )

    model_name = "claude-4-sonnet-20250514"
    db_id = scenario_run.devbox_id

    problem_statement = quote(scenario.input_context.problem_statement)
    await client.devboxes.execute_sync(db_id, command=f"cd /testbed && uv tool install mini-swe-agent && export MSWEA_CONFIGURED=true && export MSWEA_MODEL_NAME={model_name} && export ANTHROPIC_API_KEY={os.environ.get("ANTHROPIC_API_KEY")} && mini -y -t {problem_statement}", shell_name="my-shell")

    # Run the scoring function. Automatically marks the scenario run as done.
    # Note the async client is used here.
    validated = await client.scenarios.runs.score_and_await(scenario_run.id)
    print(validated)

asyncio.run(main())