import argparse
from benchmark_orchestrator.benchmark_utils import BuildBackends
from benchmark_orchestrator.results_handler import (
    load_results,
    summarize_results,
    visualize_results,
)


def main():
    parser = argparse.ArgumentParser(
        description="Summarize benchmark results and create visualization"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="benchmark_results.json",
        help="Input JSON file with benchmark results (default: benchmark_results.json)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="average_build_times.svg",
        help="Output SVG filename for visualization (default: average_build_times.svg)",
    )
    args = parser.parse_args()

    results = load_results(args.input)
    summarize_results(results)

    excluded_backends = [
        BuildBackends.SCIKIT,
        BuildBackends.MATURIN,
    ]

    visualize_results(results, excluded_backends, args.output)
    print(f"Visualization saved to: {args.output}")


if __name__ == "__main__":
    main()
