
import concurrent.futures

def search_key_words(file_paths: list[str], key_words: list[str], thread_count: int) -> dict[str, list[str]]:
    if len(file_paths) == 0:
        raise ValueError("file_paths can't be empty")
    
    if len(key_words) == 0:
        raise ValueError("key_words can't be empty")
    
    if thread_count <= 0:
        raise ValueError("thread_count can't be less than or equal to 0")
    
    # If the number of threads is greater than the number of files, then we will use the number of files as the number of threads
    thread_count = min(thread_count, len(file_paths))

    # Create a dictionary to store the results
    results = {key_word: [] for key_word in key_words}

    # Divide the file paths into groups
    group_size = len(file_paths) // thread_count
    file_paths_groups = [file_paths[i::group_size] for i in range(group_size)]

    # Create a thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        # Submit the tasks
        futures = {executor.submit(_search_key_words_in_files, file_paths_group, key_words) for file_paths_group in file_paths_groups}
        
        # Get the results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            for key_word in key_words:
                results[key_word].extend(result[key_word])

    return results
    

def _search_key_words_in_files(file_paths: list[str], key_words: list[str]) -> dict[str, list[str]]:
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
