from istorage import IStorage
import csv


class StorageCsv(IStorage):
    """Handles CRUD and managing movie data in a Csv file"""

    def __init__(self, file_path: str):
        """
        Initializes the StorageCsv instance to handle movie data storage in a CSV file.

        Args:
            file_path (str): Path to the CSV file used for storing movie data.

        Raises:
            ValueError: If the file_path is empty or does not have a ".csv" extension.
            TypeError: If the file_path is not a string.
        """
        file_format = file_path.split(".")[-1]
        if file_format != "csv":
            raise ValueError (f"Invalid file extension. Expected .csv file but got {file_format}")
        super().__init__(file_path)



    def read_movies(self):
        """
        Reads movie data from the Csv file.

        The function reads the CSV file, extracts the movie data, and organizes it into
        a dictionary where the keys are the movie titles and the values are dictionaries
        containing the movie's details (year, rating, poster_url).

        Returns:
            dict: Dictionary containing the movie data to read.

        Handles:
            FileNotFoundError: If the file does not exist, returns an empty dictionary.
            csv.Error: If the file is not in valid Csv format, returns an empty dictionary.
        """
        try:
            with open(self.file_path, "r") as handle:
                reader = csv.DictReader(handle)

                data = {}
                for row in reader:
                    title = row["title"]
                    del row["title"]
                    data[title] = row
        except FileNotFoundError:
            print(f"File {self.file_path} was not found.")
            data = {}
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
            data = {}
        return data


    def write_movies(self, data: dict):
        """
        Writes/Overwrites movie data to the Csv file.

        This function takes a dictionary containing the movie data and writes it to a CSV file.
        It overwrites any existing content in the file.

        Args:
            data (dict): Dictionary containing the movie data to save.

        Handles:
            IOError: If there is an error while writing to the file. Like no permission.
        """
        try:
            with open(self.file_path, 'w', newline='') as handle:
                first_movie = list(data.values())[0]
                fieldnames = ['title'] + list(first_movie.keys())
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                rows = []
                for title, info in data.items():
                    row = {'title': title}
                    row.update(info)
                    rows.append(row)
                writer.writerows(rows)
            print("CSV file was successfully created.")
        except IOError as e:
            print(f"Error writing to file: {e}")






















