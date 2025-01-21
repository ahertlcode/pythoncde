import os

def count_files_in_directory(directory):
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

# Specify the directory path here
directory_path = "EXAM_SCORE"

total_files = count_files_in_directory(directory_path)
print(f"Total number of files: {total_files}")
