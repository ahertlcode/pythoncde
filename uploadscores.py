import os
import requests

# Laravel endpoint URL for mass upload
upload_url = "http://localhost:8000/api/scores/upload"

# Root directory containing subdirectories with Excel files
root_directory_path = "FIXES-SSS1"

# Authentication token if required (replace with actual token)

# Walk through the root directory and its subdirectories
for dirpath, dirnames, filenames in os.walk(root_directory_path):
    for filename in filenames:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):  # Ensure only Excel files are processed
            file_path = os.path.join(dirpath, filename)
            try:
                # Open the file in binary mode
                with open(file_path, 'rb') as file:
                    # Prepare file data for upload
                    files = {'file': (filename, file)}

                    # Send POST request to upload the file
                    response = requests.post(upload_url, headers={}, files=files)

                    # Check response
                    if response.status_code == 200:
                        print(f"Uploaded: {file_path}")
                    else:
                        print(f"Failed to upload: {file_path} - {response.status_code} {response.text}")
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")
