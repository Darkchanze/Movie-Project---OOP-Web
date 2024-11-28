
from istorage import IStorage
import csv


class StorageCsv(IStorage):
    """Handles CRUD and managing movie data in a Csv file"""

    def __init__(self, file_path: str):
        """
        Initializes the StorageCsv instance.

        Args:
            file_path (str): Path to the Csv file used for storage of movies_data

        Raises:
            ValueError: If the file_path is empty or does not have a ".csv" extension.
            TypeError: If the file_path is not a string.
        """
        if file_path.strip() == "":
            raise ValueError ("Given file_path must not be empty!")
        file_format = file_path.split(".")[-1]
        if file_format != "csv":
            raise ValueError (f"Invalid file extension. Expected .csv file but got {file_format}")
        if not isinstance(file_path, str):
            raise TypeError (f"Given file_path must be a string! Input was {type(file_path)}.")
        self.file_path = file_path.strip()


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


    def list_movies(self):
        """
        Prints all movies stored in the JSON file along with their year and rating.
        """
        movies_data_dict = self.read_movies()
        print(f"{len(movies_data_dict)} movies in total:")
        for name, value in movies_data_dict.items():
            print(f"{name} ({value['year']}): {value['rating']}")


    def add_movie(self, title: str, year: str, rating: str, poster_url: str):
        """
        Adds a new movie to the json file of the instance.

        Args:
            title (str): Title of the movie.
            year (int): Release year of the movie.
            rating (float): Rating of the movie.
            poster_url (str): URL to the movie's poster image.

        Raises:
            ValueError: If any of the inputs fail validation. This is checked with the validate functions.
        """
        movies_data_dict = self.read_movies()
        movies_data_dict[title] = {}
        movies_data_dict[title]['year'] = year
        movies_data_dict[title]['rating'] = rating
        movies_data_dict[title]['poster_url'] = poster_url
        print(f"Movie {title} successfully added")
        self.write_movies(movies_data_dict)


    def delete_movie(self, title: str):
        """
        Deletes a new movie to the json file of the instance.

        Args:
            title (str): Title of the movie to delete.

        Prints:
            Success or failure message indicating if the movie was found and deleted.

        Raises:
            ValueError: If the title input fails validation.
        """
        movies_data_dict = self.read_movies()
        self.validate_title(title)
        movie = next((movie for movie in movies_data_dict if movie.lower() == title.lower()), None)
        if movie:
            del movies_data_dict[movie]
            print(f"Movie {movie} successfully deleted")
        else:
            print(f"Movie {title} doesn't exist!")
        self.write_movies(movies_data_dict)


    def update_movie(self, title: str, rating: float):
        """
        Update a new movie to the json file of the instance.

        Args:
            title (str): Title of the movie to update.
            rating (float): New rating for the movie.

        Prints:
            Success or failure message indicating, if the movie was found and updated.

        Raises:
            ValueError: If the title or rating input fails validation.
        """
        movies_data_dict = self.read_movies()
        self.validate_title(title)
        self.validate_rating(rating)
        movie = next((movie for movie in movies_data_dict if movie.lower() == title.lower()), None)
        if movie:
            movies_data_dict[movie]["rating"] = rating
            print(f"Movie {movie} successfully updated")
        else:
            print(f"Movie {movie} doesn't exist!")
        self.write_movies(movies_data_dict)


    def validate_title(self, title: str):
        """
        Validates the title input.

        Args:
            title (str): Title of the movie.

        Raises:
            ValueError: If the title is not a string.
        """
        if not isinstance(title, str):
            raise ValueError(f"Title must be an string, got {type(title)}")


    def validate_rating(self, rating: float):
        """
        Validates the rating input.

        Args:
            rating (float): Rating of the movie.

        Raises:
            ValueError: If the rating is not a float.
        """
        if not isinstance(rating, float):
            raise ValueError(f"Rating must be an float, got {type(rating)}")





