import shutil
from pathlib import Path

class operations:

    @staticmethod
    def copy(source_file, destination_folder):
        try:
            shutil.copy(source_file, destination_folder)
            print(f"File {source_file} copied successfully to {destination_folder}")
        except Exception as e:
            print(f"Error occurred while copying file: {e}")

    @staticmethod
    def move(source_file, destination_folder):
        try:
            shutil.move(source_file, destination_folder)
            print(f"File {source_file} moved successfully to {destination_folder}")
        except Exception as e:
            print(f"Error occurred while moving file: {e}")

    @staticmethod
    def delete(self, file_path):
        try:
            Path(file_path).unlink()
            print(f"File {file_path} deleted successfully")
        except Exception as e:
            print(f"Error occurred while deleting file: {e}")

    @staticmethod
    def rename(self, old_directory_path, new_directory_name):
        try:
            shutil.move(
                old_directory_path, f"{old_directory_path}/{new_directory_name}"
            )
            print(
                f"Directory {old_directory_path} renamed to {new_directory_name} successfully"
            )
        except Exception as e:
            print(f"Error occurred while renaming directory: {e}")

    @staticmethod
    def create_dir(
        self, directory_path
    ):  # Creates a new directory at the specified path
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            print(f"Directory {directory_path} created successfully")
        except Exception as e:
            print(f"Error occurred while creating directory: {e}")

    @staticmethod
    def list(directory_path):  # Lists all files in the specified directory
        try:
            for file in Path(directory_path).iterdir():
                if file.is_file():
                    print(file.name)
        except Exception as e:
            print(f"Error occurred while listing files in directory: {e}")

    @staticmethod
    def zip(
        source_directory, destination_zip_file
    ):  # Compresses all files in the specified
        try:
            shutil.make_archive(destination_zip_file, "zip", source_directory)
            print(
                f"Files in directory {source_directory} zipped successfully to {destination_zip_file}"
            )
        except Exception as e:
            print(f"Error occurred while zipping files: {e}")


