from storage.istorage import IStorage
import json



class StorageJson(IStorage):
    """Handles CRUD and managing movie data in a JSON file"""

    def __init__(self, file_path: str):
        """
        Initializes the StorageJson instance to handle movie data storage in a json file.

        Args:
            file_path (str): Path to the json file used for storing movie data.

        Raises:
            ValueError: If the file_path is empty or does not have a ".json" extension.
            TypeError: If the file_path is not a string.
        """
        file_format = file_path.split(".")[-1]
        if file_format != "json":
            raise ValueError (f"Invalid file extension. Expected .json file but got {file_format}")
        super().__init__(file_path)


    def read_movies(self):
        """
        Reads movie data from the JSON file.

        Returns:
            dict: Dictionary containing the movie data to read.

        Handles:
            FileNotFoundError: If the file does not exist, returns an empty dictionary.
            JSONDecodeError: If the file is not in valid JSON format, returns an empty dictionary.
        """
        try:
            with open(self.file_path , "r") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as e:
            print(f"Data type was not in JSON format: {e}")
            data = {}
        except FileNotFoundError:
            print(f"File {self.file_path} was not found.")
            data = {}
        return data


    def write_movies(self, data: dict):
        """
        Writes/Overwrites movie data to the JSON file.

        Args:
            data (dict): Dictionary containing the movie data to save.

        Handles:
            IOError: If there is an error while writing to the file. Like no permission.
        """
        try:
            with open(self.file_path , "w") as handle:
                json.dump(data ,handle, indent = 4)
        except IOError as e:
            print(f"Error at opening file: {e}")




































