import statistics
import random
from API_Movies import api_request_data
from storage_json import StorageJson
from storage_csv import StorageCsv

class MovieApp:
    """user input is validated and the user can choose different commands."""


    def __init__(self, storage):
        """
        Initializes where the data is taken from. Json or CSV.

        Args:
            storage: The storage object responsible for handling movie data.
        """
        self.storage = storage


    def run(self):
        """
        Run the main menu for the application, allowing users to choose commands.

        This function repeatedly displays a menu until the user decides to exit.
        """
        print("********** My Movies Database **********")
        in_menu = True
        while in_menu:
            movies = self.storage.read_movies()
            menu_functions = {
                0: self.exit_menu,
                1: self.list_movies,
                2: self.add_movie,
                3: self.delete_movie,
                4: self.update_movie,
                5: self.show_stats,
                6: self.print_random_movie,
                7: self.search_movies,
                8: self.print_movies_sorted_by_rating,
                9: self.print_movies_sorted_by_year,
                10: self.filter_movie,
            }
            try:
                print("""
        Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Movies sorted by year
        10. Filter movies

        Enter choice (0-10): """, end='')
                user_menu_choice = int(input(''))
                print()
                if 0 <= user_menu_choice <= 10:
                    if user_menu_choice == 0:
                        in_menu = menu_functions[user_menu_choice]()
                        break
                    elif user_menu_choice in {1, 3, 4}:
                        menu_functions[user_menu_choice]()
                    elif user_menu_choice in {2, 5, 6, 7, 8, 9, 10}:
                        menu_functions[user_menu_choice](movies)
                        print()
                else:
                    print(f"The number must be between 0 and {len(menu_functions)}.")
            except Exception:
                print(f"Invalid choice.")
                print()
            input('Press enter to continue')


    def exit_menu(self):
        """
        Exit the Interface.

        Returns:
            bool: False, to indicate the program should terminate, the while loop will break in run().
        """
        print("Bye!")
        return False


    def list_movies(self):
        """Lists all movies of the instance of the user"""
        self.storage.list_movies()


    def add_movie(self, movies: dict):
        """
        Add a new movie to the user's collection.

        Args:
            movies (dict): A dictionary of the user's current movies, where the
                           keys are movie titles and the values contain movie details.
        """
        api_data = self.get_movie_name_and_fetch_info_from_api(movies)
        if api_data:
            title, year, rating, poster_url = api_data
        else:
            return
        self.storage.add_movie(title, year, rating, poster_url)


    def delete_movie(self):
        """
        Deletes a movie form the instance of the user.

        Args:
            movies (dict): The current dictionary of movies.
        """
        movie_to_delete = input("Enter a movie to delete: ")
        self.storage.delete_movie(movie_to_delete)


    def update_movie(self):
        """
        Updates the rating of a movie form the instance of the user.

        Prompts the user for the movie name and the new rating, then updates the data in storage.
        """
        movie_to_update = input("Enter a movie to update: ")
        rating = self.get_new_movie_rating()
        self.storage.update_movie(movie_to_update, rating)


    def get_movie_name_and_fetch_info_from_api(self, movies: dict):
        """
        Prompt the user to enter a movie name, fetch its details from an API,
        and ensure it is not already in the movie collection.

        Args:
            movies (dict): A dictionary with existing movies,
                           where the keys are the movie titles.

        Returns:
            tuple: A tuple containing the movie details fetched from the API:
                   (title (str), year (str), rating (str), poster_url (str)).
                   These details are only returned if the movie is valid and
                   not already in the collection.
        """
        while True:
            new_movie = input("Enter new movie name: ").strip()
            if not new_movie:
                print("Movie name must not be empty.")
                continue
            api_data = api_request_data(new_movie)
            if api_data:
                title, year, rating, poster_url = api_data
            else:
                return False
            if title in movies:
                print(f"Movie {title} already exist!")
            else:
                return api_data



    def get_new_movie_rating(self):
        """
        Prompt the user to enter a rating for a new movie.

        Returns:
            float: The rating of the new movie.
        """
        while True:
            try:
                new_movie_rating = float(input("Enter new movie rating: "))
                return new_movie_rating
            except ValueError:
                print("Please enter a valid rating.")


    def show_stats(self, movies: dict):
        """
        Display statistics about the movies of the user instance.

        Args:
            movies (dict): The current dictionary of movies.

        Prints:
            - Average rating
            - Median rating
            - Best movie
            - Worst movie
        """
        list_of_ratings = [movie['rating'] for movie in movies.values()]
        print(f"Average rating: {round(statistics.mean(list_of_ratings), 1)}")
        print(f"Median rating: {round(statistics.median(list_of_ratings), 1)}")
        self.print_best_movie(movies)
        self.print_worst_movie(movies)


    def print_best_movie(self, movies: dict):
        """
         Print the best rated movie from the user instance.

         Args:
             movies (dict): The current dictionary of movies.
         """
        movies_sorted_rating = self.movies_sorted_by_rating(movies)
        last_movie_rating = movies[movies_sorted_rating[0]]['rating']
        for movie in movies_sorted_rating:
            if last_movie_rating <= movies[movie]['rating']:
                print(f"Best movie: {movie}, {movies[movie]['rating']}")
                last_movie_rating = movies[movie]['rating']
            else:
                break


    def print_worst_movie(self, movies: dict):
        """
         Print the worst rated movie from the user instance.

         Args:
             movies (dict): The current dictionary of movies.
         """
        movies_sorted_rating = self.movies_sorted_by_rating(movies)
        movies_sorted_rating.reverse()
        last_movie_rating = movies[movies_sorted_rating[0]]['rating']
        for movie in movies_sorted_rating:
            if last_movie_rating >= movies[movie]['rating']:
                print(f"Worst movie: {movie}, {movies[movie]['rating']}")
                last_movie_rating = movies[movie]['rating']
            else:
                break


    def movies_sorted_by_rating(self, movies: dict):
        """
        Returns a list sorted by ratings from highest to lowest.

        Args:
            movies (dict): The current dictionary of movies.

        Returns:
            list: A list of movie names sorted by rating, highest to lowest.
        """
        movies_sorted_rating = sorted(movies, key=lambda movie: movies[movie]['rating'], reverse=True)
        return movies_sorted_rating


    def print_random_movie(self, movies: dict):
        """
         Print a randomly selected movie from the user instance.

         Args:
             movies (dict): The current dictionary of movies.
         """
        random_movie = random.choice(list(movies.keys()))
        print(f"Your movie for tonight: {random_movie}, it's rated {movies[random_movie]['rating']}")


    def search_movies(self, movies: dict):
        """
        Get user input and search for a movie name(part) and print all related movies, case-insensitive.

        Args:
            movies (dict): The current dictionary of movies.

        Prints:
            Movies matching the keyword (case-insensitive).
        """
        search_movie = input("Enter part of movie name: ")
        for movie in movies:
            if search_movie.lower() in movie.lower():
                print(f"{movie}, {movies[movie]['rating']}")


    def print_movies_sorted_by_year(self, movies: dict):
        """
        Print movies sorted by their release year, either ascending or descending.

        Args:
            movies (dict): The current dictionary of movies.
        """
        movies_sorted_year = self.movies_sorted_by_year(movies)
        while True:
            user_choice = input("Do you want the latest movies first? (Y/N)").lower()
            if user_choice == "y":
                movies_sorted_year.reverse()
                for movie in movies_sorted_year:
                    print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")
                break
            elif user_choice == "n":
                for movie in movies_sorted_year:
                    print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")
                break
            else:
                print('Please enter "Y" or "N"')


    def print_movies_sorted_by_rating(self, movies: dict):
        """
        Print movies sorted by their ratings in descending order.

        Args:
            movies (dict): The current dictionary of movies.
        """
        movies_sorted_rating = self.movies_sorted_by_rating(movies)
        for movie in movies_sorted_rating:
            print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")


    def movies_sorted_by_year(self, movies: dict):
        """
        Sorts the list of movies by year from highest to lowest.

        Args:
            movies (dict): The current dictionary of movies.

        Returns:
            list: A list of movie names sorted by year, oldest to newest.
        """
        movies_sorted_year = sorted(movies, key=lambda movie: movies[movie]['year'])
        return movies_sorted_year


    def filter_movie(self, movies: dict):
        """
        Filter movies based on user input. Based on minimum rating, start year, end year

        Args:
            movies (dict): The current dictionary of movies.

        Prints:
            A filtered list of movies matching the criteria.
        """
        minimum_rating = self.get_movie_rating()
        start_year = self.get_movie_year("start")
        end_year = self.get_movie_year("end")
        movies_to_delete = set()
        if minimum_rating != "":
            for movie in movies:
                if minimum_rating > movies[movie]["rating"]:
                    movies_to_delete.add(movie)
        if start_year != "":
            for movie in movies:
                if start_year > movies[movie]["year"]:
                    movies_to_delete.add(movie)
        if end_year != "":
            for movie in movies:
                if end_year < movies[movie]["year"]:
                    movies_to_delete.add(movie)
        for movie_to_delete in movies_to_delete:  # movies_copy
            del movies[movie_to_delete]
        print(movies)


    def get_movie_rating(self):
        """
        Prompt the user to enter a minimum rating for filtering movies.

        Returns:
            float or str: The minimum rating entered by the user, or an empty string if left blank.
        """
        while True:
            try:
                new_movie_rating = input("Enter minimum rating (leave blank for no minimum rating):")
                if new_movie_rating == "":
                    break
                else:
                    new_movie_rating = float(new_movie_rating)
                    break
            except ValueError:
                print("Please enter a valid rating.")
        return new_movie_rating


    def get_movie_year(self, text_start_end: str):
        """
        Prompt the user to enter a year (start or end) for filtering movies.

        Args:
            text_start_end (str): User input which is end or start year.

        Returns:
            int or str: The year entered by the user, or an empty string if left blank.
        """
        while True:
            try:
                new_movie_rating = input(f"Enter {text_start_end} year (leave blank for no start year): ")
                if new_movie_rating == "":
                    break
                else:
                    new_movie_rating = int(new_movie_rating)
                    break
            except ValueError:
                print("Please enter a valid rating.")
        return new_movie_rating


    def _generate_website(self):
        """"""
        pass


    def _command_movie_show_stats(self):
        """"""
        pass


# todo Public, not public? _ or not!
# todo Maybe kuck das alles case sensitive ist vor allem bei CRUD, da is bissl gemixt auf der seite und storage json!



