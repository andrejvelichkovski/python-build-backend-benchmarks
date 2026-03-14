import matplotlib.pyplot as plt
import json
from pathlib import Path

from benchmark_orchestrator.benchmark_utils import BuildBackends
import seaborn as sns


def store_results(results: dict[str, list[float]], output_file):
    json_result = json.dumps(results, indent=4)
    with open(output_file, "w") as f:
        f.write(json_result)


def load_results(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


def summarize_results(results: dict[str, list[float]]) -> None:
    # Skip the first run to accommodate for caching and warm-up
    results = {backend: times[1:] for backend, times in results.items()}

    print("------------------------------------")
    print("Average times:")
    for backend, times in results.items():
        avg_time = sum(times) / len(times)
        print(f"{backend}: {avg_time:.2f}s")

    print("------------------------------------")
    print("p90 times:")
    for backend, times in results.items():
        p90_time = sorted(times)[int(0.9 * len(times)) - 1]
        print(f"{backend}: {p90_time:.2f}s")
    print("------------------------------------")


def visualize_results(
    results: dict[str, list[float]],
    exclude_backends: list[BuildBackends],
    output_file: str = "average_build_times.svg",
) -> None:

    backends = [
        backend for backend in list(results.keys()) if backend not in exclude_backends
    ]

    times = [sum(results[backend]) / len(results[backend]) for backend in backends]
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=backends, y=times, palette="viridis")
    plt.xlabel("Build Backends")
    plt.ylabel("Average Time (s)")
    plt.title("Average Build Times for Different Build Backends")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_file, format="svg")
    plt.close()
