import os
import json

class FileManager:
    def __init__(self, directory):
        self.directory = directory

    def list_files(self):
        try:
            files = os.listdir(self.directory)
            print("Files in directory:")
            for file in files:
                print(file)
        except Exception as e:
            print(f"An error occurred while listing files: {e}")

    def display_file_content(self, file_name):
        try:
            file_path = os.path.join(self.directory, file_name)
            if not os.path.exists(file_path):
                print(f"File {file_name} does not exist.")
                return

            with open(file_path, 'r') as file:
                content = json.load(file)
                print(json.dumps(content, indent=4))
        except Exception as e:
            print(f"An error occurred while reading file {file_name}: {e}")

    def display_attachments(self):
        try:
            files = os.listdir(self.directory)
            for file in files:
                if file.endswith("png"):
                    print(file)
        except Exception as e:
            print(f"An error occurred while listing attachment files: {e}")

    def save_to_file(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f)

    def save_attachment(self, file_name, data):
        with open(file_name, 'wb') as f:
            f.write(data)