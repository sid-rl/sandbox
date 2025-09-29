import os
import asyncio
from runloop_api_client import AsyncRunloop
from minisweagent.agents.default import DefaultAgent
from minisweagent.models import get_model
from minisweagent.environments.local import LocalEnvironment
from runloop_api_client.types.scenario_run_view import ScenarioRunView

client = AsyncRunloop(bearer_token=os.environ.get("RUNLOOP_API_KEY"))

async def run_full_benchmark():
    # Start a full run of the benchmark
    benchmark_id = "bmd_2zmp3Mu3LhWu7yDVIfq3m"
    benchmark = await client.benchmarks.retrieve(benchmark_id)
    benchmark_run = await client.benchmarks.start_run(
        benchmark_id=benchmark_id,
        run_name="SWE-bench_Verified mini-swe-agent test",
    )

    print(f"Benchmark run: {benchmark_run.id} {benchmark_run.name}")

    results = await asyncio.gather(*[attempt_scenario_run(client, scenario_id, benchmark_run.id) for scenario_id in benchmark.scenario_ids])

    # Optionally end the benchmark run early (runs auto-complete when pending scenarios are done)
    result = await client.benchmarks.runs.complete(benchmark_run.id)
    print(result)

async def attempt_scenario_run(client: AsyncRunloop, scenario_id: str, benchmark_run_id: str | None) -> ScenarioRunView:
    scenario = await client.scenarios.retrieve(scenario_id)
    scenario_run = await client.scenarios.start_run_and_await_env_ready(
        scenario_id=scenario_id,
        benchmark_run_id=benchmark_run_id,
        run_name=f"{scenario.name} mini-swe-agent test run",
    )
    model_name = "claude-sonnet-4-20250514"
    problem_statement = scenario.input_context.problem_statement
    my_agent = DefaultAgent(
        get_model(input_model_name=model_name),
        LocalEnvironment(),
    )
    my_agent.run(problem_statement)
    result = await client.scenarios.runs.score_and_await(scenario_run.id)
    return result


asyncio.run(run_full_benchmark())