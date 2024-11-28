from istorage import IStorage
import json


class StorageJson(IStorage):
    """Handles CRUD and managing movie data in a JSON file"""

    def __init__(self, file_path: str):
        """
        Initializes the StorageCsv instance.

        Args:
            file_path (str): Path to the Csv file used for storage of movies_data

        Raises:
            ValueError: If the file_path is empty or does not have a ".json" extension.
            TypeError: If the file_path is not a string.
        """
        if file_path.strip() == "":
            raise ValueError ("Given file_path must not be empty!")
        file_format = file_path.split(".")[-1]
        if file_format != "json":
            raise ValueError (f"Invalid file extension. Expected .json file but got {file_format}")
        if not isinstance(file_path, str):
            raise TypeError (f"Given file_path must be a string! Input was {type(file_path)}.")
        self.file_path = file_path.strip()


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
            year (str): Release year of the movie.
            rating (str): Rating of the movie.
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


    def validate_year(self, year: int):
        """
        Validates the year input.

        Args:
            year (int): Release year of the movie.

        Raises:
            ValueError: If the year is not an integer.
        """
        if not isinstance(year, int):
            raise ValueError(f"Year must be an integer, got {type(year)}")


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



    def validate_poster_url(self, poster_url: str):
        """
        Validates the poster URL input.

        Args:
            poster_url (str): URL to the movie's poster image.

        Raises:
            ValueError: If the poster URL is not a string.
        """
        if not isinstance(poster_url, str):
            raise ValueError(f"Poster_url must be an string, got {type(poster_url)}")


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







