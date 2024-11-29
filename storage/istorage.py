from abc import ABC, abstractmethod
import os
class IStorage(ABC):
    """Abstract parent class defining the interface of movie storage child classes."""

    def __init__(self, file_path: str):
        """
        Initializes the IStorage instance.

        Args:
            file_path (str): The path to the storage file for the movie data.

        Raises:
            ValueError: If the provided file_path is an empty string.
            TypeError: If the provided file_path is not a string.
        """
        if file_path.strip() == "":
            raise ValueError("Given file_path must not be empty!")
        if not isinstance(file_path, str):
            raise TypeError(f"Given file_path must be a string! Input was {type(file_path)}.")
        folder_path = "data"
        os.makedirs(folder_path, exist_ok=True)

        self.file_path = os.path.join(folder_path, file_path.strip())


    @abstractmethod
    def read_movies(self):
        """Reads movie data from the chosen file extension."""
        pass


    @abstractmethod
    def write_movies(self, data: dict):
        """Writes/Overwrites movie data to the chosen file extension."""
        pass


    def list_movies(self):
        """
        Prints all movies stored in the file-type along with their year and rating.
        """
        movies_data_dict = self.read_movies()
        print(f"{len(movies_data_dict)} movies in total:")
        for name, value in movies_data_dict.items():
            print(f"{name} ({value['year']}): {value['rating']}")


    def add_movie(self, title: str, year: str, rating: str, poster_url: str):
        """
        Adds a new movie to the file-type file of the instance.

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
        Deletes a new movie to the file-type of the instance.

        Args:
            title (str): Title of the movie to delete.

        Prints:
            Success or failure message indicating if the movie was found and deleted.

        Raises:
            ValueError: If the title input fails validation.
        """
        movies_data_dict = self.read_movies()
        self._validate_title(title)
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
        self._validate_title(title)
        self._validate_rating(rating)
        movie = next((movie for movie in movies_data_dict if movie.lower() == title.lower()), None)
        if movie:
            movies_data_dict[movie]["rating"] = rating
            print(f"Movie {movie} successfully updated")
        else:
            print(f"Movie {movie} doesn't exist!")
        self.write_movies(movies_data_dict)


    def _validate_title(self, title: str):
        """
        Validates the title input.

        Args:
            title (str): Title of the movie.

        Raises:
            ValueError: If the title is not a string.
        """
        if not isinstance(title, str):
            raise ValueError(f"Title must be an string, got {type(title)}")


    def _validate_rating(self, rating: float):
        """
        Validates the rating input.

        Args:
            rating (float): Rating of the movie.

        Raises:
            ValueError: If the rating is not a float.
        """
        if not isinstance(rating, float):
            raise ValueError(f"Rating must be an float, got {type(rating)}")