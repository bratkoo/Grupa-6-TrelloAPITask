import json
import os


class FileReader:
    def __init__(self, directory):
        self.directory = directory

    def list_files(self):
        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        return files

    def read_file(self, filename):
        with open(os.path.join(self.directory, filename), 'r') as f:
            data = json.load(f)
        return data

    def print_file_content(self, filename):
        data = self.read_file(filename)
        print(json.dumps(data, indent=4))


def main():
    reader = FileReader('.')
    files = reader.list_files()
    print("Fajlovi:")
    for file in files:
        print(file)




    #filename = input("Enter the filename to display content: ")
    #reader.print_file_content(filename)


if __name__ == '__main__':
    main()
