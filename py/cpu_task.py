import argparse
import sys
import sysconfig
import time
from concurrent.futures import ThreadPoolExecutor


def cpu_bound_task_sum(n):
    """A CPU-bound task that computes the sum of squares up to n."""
    num = sum(i * i for i in range(n))
    return num

def cpu_bound_task(n):
    if n <= 1:
        return n
    return cpu_bound_task(n-1) + cpu_bound_task(n-2)

def main():
    parser = argparse.ArgumentParser(description="Run a CPU-bound task with threads")
    parser.add_argument("--threads", type=int, default=4, help="Number of threads")
    parser.add_argument("--tasks", type=int, default=10, help="Number of tasks")
    parser.add_argument(
        "--size", type=int, default=35, help="Fibonacci number to compute (n for nth Fibonacci number)"
    )
    args = parser.parse_args()
    print(f"Python Version: {sys.version}")

    # Check GIL status
    py_version = float(".".join(sys.version.split()[0].split(".")[0:2]))
    status = sysconfig.get_config_var("Py_GIL_DISABLED")

    if py_version >= 3.13:
        status = sys._is_gil_enabled()
    if status is None:
        print("GIL cannot be disabled for Python version <= 3.12")
    if status == 0:
        print("GIL is currently disabled")
    if status == 1:
        print("GIL is currently active")

    print(f"Running {args.tasks} tasks of size {args.size} with {args.threads} threads")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        list(executor.map(cpu_bound_task, [args.size] * args.tasks))
    end_time = time.time()
    duration = end_time - start_time

    print(f"Time with threads: {duration:.2f} seconds")


if __name__ == "__main__":
    main()
