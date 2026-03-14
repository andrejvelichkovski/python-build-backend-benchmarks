import argparse
from pathlib import Path

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
    # Disabling the Maturin and Scikit backends for now as their performance
    # is below the others as their use cases are specific.
    # BuildBackends.MATURIN,
    # BuildBackends.SCIKIT,
]

BENCHMARK_REPETITIONS = 20


def main():
    parser = argparse.ArgumentParser(description="Run build backend benchmarks")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="benchmark_results.json",
        help="Output filename for benchmark results (default: benchmark_results.json)",
    )
    parser.add_argument(
        "--repetitions",
        "-r",
        type=int,
        default=3,
        help="Number of benchmark repetitions (default: 20)",
    )
    args = parser.parse_args()

    average_times = {}
    benchmark_results = {}

    for backend in all_backends:
        print(f"Setting up project with build backend: {backend}")

        project_path = f"../build-benchmark-project-{backend}"

        setup_project(backend, project_path)
        time_taken = benchmark_project(project_path, args.repetitions)

        benchmark_results[backend] = time_taken

        clean_benchmark(project_path)

    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    store_results(benchmark_results, results_dir / args.output)
    print(f"Results saved to: results/{args.output}")


if __name__ == "__main__":
    main()
