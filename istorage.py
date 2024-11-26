from abc import ABC, abstractmethod

class IStorage(ABC):
    """Abstract parent class defining the interface of movie storage child classes."""

    @abstractmethod
    def list_movies(self):
        """Lists all movies in the instance"""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Adds a movie to the instance"""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from the instance"""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Updates a movie rating from the instance"""
        pass