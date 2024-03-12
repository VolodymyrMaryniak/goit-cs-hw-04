from pathlib import Path
import time
import threading_key_words_search


def get_file_paths(directory: str) -> list[str]:
    directory_path = Path(directory)
    txt_files = [str(file).replace("\\", "/") for file in directory_path.glob("*.txt")]
    return txt_files


def main():

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
    result = threading_key_words_search.search_key_words(file_paths, key_words, 3)
    end_time = time.time()

    execution_time_ms = (end_time - start_time) * 1000
    print(
        f"\nMultithreading approach execution time: {execution_time_ms} milliseconds\n"
    )
    display_results(result)

    start_time = time.time()
    # TODO: Update it with multiprocessing approach
    result = threading_key_words_search.search_key_words(
        file_paths, key_words, 3
    ) 
    end_time = time.time()

    execution_time_ms = (end_time - start_time) * 1000
    print(
        f"\nMultiprocessing approach execution time: {execution_time_ms} milliseconds\n"
    )
    display_results(result)


def display_results(result: dict[str, list[str]]):
    for key_word, files in result.items():
        if files:
            print(f'"{key_word}": {files}')


if __name__ == "__main__":
    main()
