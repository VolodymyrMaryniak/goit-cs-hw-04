from concurrent.futures import Executor, as_completed
from typing import Callable


def concurrent_key_words_search(
    file_paths: list[str],
    key_words: list[str],
    workers_count: int,
    executor_factory: Callable[[int], Executor],
) -> dict[str, list[str]]:

    if len(file_paths) == 0:
        raise ValueError("file_paths can't be empty")

    if len(key_words) == 0:
        raise ValueError("key_words can't be empty")

    if workers_count <= 0:
        raise ValueError("workers_count can't be less than or equal to 0")

    # If the number of workers is greater than the number of files, then we will use the number of files as the number of threads
    workers_count = min(workers_count, len(file_paths))

    # Divide the file paths into groups
    file_paths_groups = [file_paths[i::workers_count] for i in range(workers_count)]

    # Create an executor (ThreadPoolExecutor, ProcessPoolExecutor, etc.)
    with executor_factory(workers_count) as executor:
        return _execute_key_words_search(executor, file_paths_groups, key_words)


def _execute_key_words_search(
    executor: Executor, file_paths_groups: list[list[str]], key_words: list[str]
):
    results = {key_word: [] for key_word in key_words}

    # Submit the tasks
    futures = {
        executor.submit(_search_key_words_in_files, file_paths_group, key_words)
        for file_paths_group in file_paths_groups
    }

    # Get the results
    for future in as_completed(futures):
        result = future.result()
        for key_word in key_words:
            results[key_word].extend(result[key_word])

    return results


def _search_key_words_in_files(
    file_paths: list[str], key_words: list[str]
) -> dict[str, list[str]]:
    results = {key_word: set() for key_word in key_words}
    for file_path in file_paths:
        try:
            with open(file_path, "r") as file:
                for line in file:
                    for key_word in key_words:
                        if key_word in line:
                            results[key_word].add(file_path)
                            break
        except Exception as e:
            print(f"An error occurred while processing the file {file_path}: {e}")

    return results
