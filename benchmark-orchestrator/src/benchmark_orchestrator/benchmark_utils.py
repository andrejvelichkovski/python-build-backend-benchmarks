import subprocess
import time


PYTHON_VERSION = "3.14"


class BuildBackends:
    UV = "uv"
    PDM = "pdm"
    POETRY = "poetry"
    HATCH = "hatch"
    SETUPTOOLS = "setuptools"
    MATURIN = "maturin"
    SCIKIT = "scikit"


def setup_project(build_backend: BuildBackends, project_directory: str) -> None:
    """
    Setups an empty Python project using UV. It initializes a new UV project,
    creates a virtual environment, and installs the necessary dependencies
    for the benchmark orchestrator. This function is intended to be run
    once to set up the project environment before running any benchmarks.
    """

    # Check if project directory exists, if not create it
    subprocess.run(["mkdir", "-p", project_directory], check=True)

    # Initialize a new UV project
    subprocess.run(
        [
            "uv",
            "init",
            "--package",
            "-p",
            PYTHON_VERSION,
            "--no-readme",
            "--build-backend",
            build_backend,
        ],
        check=True,
        cwd=project_directory,
    )

    print(f"Initialized a new UV project with build backend: {build_backend}")


# todo: fix type
def benchmark_project(
    project_directory: str, benchmark_repetitions: int
) -> list[float]:
    """
    Benchmarks the project using UV. It runs the benchmark command in the
    specified project directory. This function is intended to be run after
    setting up the project environment and adding the necessary benchmark
    scripts and dependencies.
    """

    times = []

    for _ in range(benchmark_repetitions):

        # Run the benchmark command and measure time
        start = time.perf_counter()
        subprocess.run(
            ["uv", "build", "--quiet"],
            check=True,
            cwd=project_directory,
        )
        end = time.perf_counter()

        times.append(end - start)

    return times


def clean_benchmark(project_directory: str) -> None:
    """
    Cleans the benchmark artifacts from the project directory. This function
    is intended to be run after benchmarking to remove any build artifacts
    and reset the project environment for future benchmarks.
    """

    subprocess.run(["rm", "-rf", project_directory], check=True)
