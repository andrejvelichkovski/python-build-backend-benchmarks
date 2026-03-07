from benchmark_orchestrator.benchmark_utils import BuildBackends
from benchmark_orchestrator.results_handler import (
    load_results,
    summarize_results,
    visualize_results,
)


results = load_results("benchmark_results.json")
summarize_results(results)

excluded_backends = [
    BuildBackends.SCIKIT,
    BuildBackends.MATURIN,
]

visualize_results(results, excluded_backends)
