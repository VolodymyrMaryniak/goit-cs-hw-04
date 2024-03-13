import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
from typing import Callable

from key_words_search import concurrent_key_words_search


def main():
    # Multithreading approach
    test_approach(
        "Multithreading", 3, lambda workers_count: ThreadPoolExecutor(workers_count)
    )

    # Multiprocessing approach
    test_approach(
        "Multiprocessing", 3, lambda workers_count: ProcessPoolExecutor(workers_count)
    )


def test_approach(
    approach_name: str, workers_count: int, executor_factory: Callable[[int], Executor]
):
    file_paths = get_file_paths("text_files")

    key_words = [
        "multithreading",
        "concurrency",
        "processor",
        "thread",
        "mutex",
        "migration",
        "harmony",
    ]

    start_time = time.time()
    result = concurrent_key_words_search(
        file_paths, key_words, workers_count, executor_factory
    )
    end_time = time.time()

    execution_time_ms = (end_time - start_time) * 1000
    print(
        f"\n{approach_name} approach execution time: {execution_time_ms} milliseconds"
    )
    display_results(result)


def display_results(result: dict[str, list[str]]):
    for key_word, files in result.items():
        if files:
            print(f'"{key_word}": {files}')


def get_file_paths(directory: str) -> list[str]:
    directory_path = Path(directory)
    txt_files = [str(file).replace("\\", "/") for file in directory_path.glob("*.txt")]
    return txt_files


if __name__ == "__main__":
    main()
