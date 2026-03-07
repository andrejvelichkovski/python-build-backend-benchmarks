from benchmark_orchestrator.results_handler import load_results, summarize_results


results = load_results("benchmark_results.json")
summarize_results(results)
