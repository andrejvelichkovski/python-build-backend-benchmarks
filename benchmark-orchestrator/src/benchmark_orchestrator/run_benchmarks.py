from benchmark_orchestrator.benchmark_utils import (
    BuildBackends,
    benchmark_project,
    clean_benchmark,
    setup_project,
)
from benchmark_orchestrator.results_handler import store_results

all_backends = [
    BuildBackends.UV,
    BuildBackends.SETUPTOOLS,
    BuildBackends.PDM,
    BuildBackends.POETRY,
    BuildBackends.HATCH,
    BuildBackends.MATURIN,
    BuildBackends.SCIKIT,
]

BENCHMARK_REPETITIONS = 20

average_times = {}
benchmark_results = {}

for backend in all_backends:
    print(f"Setting up project with build backend: {backend}")

    project_path = f"../build-benchmark-project-{backend}"

    setup_project(backend, project_path)
    time_taken = benchmark_project(project_path, BENCHMARK_REPETITIONS)

    average_time = sum(time_taken) / len(time_taken)

    benchmark_results[backend] = time_taken

    clean_benchmark(project_path)

store_results(benchmark_results, "benchmark_results.json")
