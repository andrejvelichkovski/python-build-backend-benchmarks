# Use Python 3.14 as base image
FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY benchmark-orchestrator /app/benchmark-orchestrator

WORKDIR /app/benchmark-orchestrator

RUN uv sync

ENTRYPOINT ["uv", "run", "python", "src/benchmark_orchestrator/run_benchmarks.py"]

CMD ["--help"]
