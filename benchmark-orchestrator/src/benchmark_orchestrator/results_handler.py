import json


def store_results(results: dict[str, list[float]], output_file):
    json_result = json.dumps(results, indent=4)
    with open(output_file, "w") as f:
        f.write(json_result)


def load_results(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


def summarize_results(results: dict[str, list[float]]) -> None:
    print("Average times:")
    for backend, times in results.items():
        avg_time = sum(times) / len(times)
        print(f"{backend}: {avg_time:.2f}s")

    print("p90 times:")
    for backend, times in results.items():
        p90_time = sorted(times)[int(0.9 * len(times)) - 1]
        print(f"{backend}: {p90_time:.2f}s")
