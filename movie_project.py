import statistics
import movie_storage
from random import choice


def menu():
    """Prints the menu, handles user input. Calls the function from the user pick over the function_dict."""
    in_menu = True
    while in_menu:
        movies = movie_storage.json_load_movies()   # Loads the movies from json into movies.
        menu_functions = {
            0: exit_menu,
            1: movie_storage.list_movies,
            2: movie_storage.add_movie,
            3: movie_storage.delete_movie,
            4: movie_storage.update_movie,
            5: show_stats,
            6: print_random_movie,
            7: search_movies,
            8: print_movies_sorted_by_rating,
            9: print_movies_sorted_by_year,
            10: filter_movie,
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
            if  0 <= user_menu_choice <= 10:
                if user_menu_choice == 0:
                    in_menu = menu_functions[user_menu_choice]()
                    break
                else:
                    menu_functions[user_menu_choice](movies)
                    print()
            else:
                print(f"The number must be between 0 and {len(menu_functions)}.")
        except Exception:
            print(f"Invalid choice.")
            print()
        input('Press enter to continue')


def check_if_movie_in_list_case_insensitive(movies, movie_to_check):
    """Checks if a movie is in the dict regardless upper- and lower-case and returns the movie in the dictionary cases. """
    movie_to_check = movie_to_check.lower()
    for movie in movies:
        if movie_to_check == movie.lower():
            movie_to_check = movie
            break
    return movie_to_check


def get_new_movie_name(movies):
    """Handles user input to get a new movie."""
    while True:
        new_movie = input("Enter new movie name: ")
        if new_movie in movies:
            print("Movie {new_movie} already exist!")
        elif new_movie:
            return new_movie
        else:
            print("Movie name must not be empty.")


def get_new_movie_year():#
    """Handles user input to get the year of the new movie."""
    while True:
        try:
            new_movie_year = int(input("Enter new movie year: "))
            return new_movie_year
        except ValueError:
            print("Please enter a valid year.")


def get_new_movie_rating():
    """Handles user input to get the rating of the new movie."""
    while True:
        try:
            new_movie_rating = float(input("Enter new movie rating: "))
            return new_movie_rating
        except ValueError:
            print("Please enter a valid rating.")


def show_stats(movies):
    """Prints the status of the movies, includes: average rating, median rating, best movie, worst movie."""
    list_of_ratings = [movie['rating'] for movie in movies.values()]
    print(f"Average rating: {round(statistics.mean(list_of_ratings),1)}")
    print(f"Median rating: {round(statistics.median(list_of_ratings),1)}")
    print_best_movie(movies)
    print_worst_movie(movies)


def print_best_movie(movies):
    """Prints the best movies."""
    movies_sorted_rating = movies_sorted_by_rating(movies)
    last_movie_rating = movies[movies_sorted_rating [0]]['rating']
    for movie in movies_sorted_rating:
        if last_movie_rating <= movies[movie]['rating']:
            print(f"Best movie: {movie}, {movies[movie]['rating']}")
            last_movie_rating = movies[movie]['rating']
        else:
            break


def print_worst_movie(movies):
    """Prints the worst movies."""
    movies_sorted_rating = movies_sorted_by_rating(movies)
    movies_sorted_rating.reverse()
    last_movie_rating = movies[movies_sorted_rating [0]]['rating']
    for movie in movies_sorted_rating:
        if last_movie_rating >= movies[movie]['rating']:
            print(f"Worst movie: {movie}, {movies[movie]['rating']}")
            last_movie_rating = movies[movie]['rating']
        else:
            break


def movies_sorted_by_rating(movies):
    """Returns a list sorted by ratings from highest to lowest."""
    movies_sorted_rating = sorted(movies, key=lambda movie: movies[movie]['rating'], reverse=True)
    return movies_sorted_rating


def print_movies_sorted_by_rating(movies):
    ########movies_sorted_by_rating(movies)
    movies_sorted_rating = movies_sorted_by_rating(movies)
    for movie in movies_sorted_rating:
        print(f"{movie} ({movies[movie]['year']}): {movies[movie]['rating']}")


def movies_sorted_by_year(movies):
    """Returns a list sorted by year from highest to lowest."""
    movies_sorted_year = sorted(movies, key=lambda movie: movies[movie]['year'])
    return movies_sorted_year


def print_movies_sorted_by_year(movies):
    """Returns a list sorted by year from starting from highest or lowest, depending on user input."""
    movies_sorted_year = movies_sorted_by_year(movies)
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


def print_random_movie(movies):
    """Print a random movie."""
    random_movie = choice(list(movies.keys()))
    print(f"Your movie for tonight: {random_movie}, it's rated {movies[random_movie]['rating']}")


def search_movies(movies):
    """Get user input and search for a movie name(part) and print all related movies, case-insensitive"""
    search_movie = input("Enter part of movie name: ")
    for movie in movies:
        if search_movie.lower() in movie.lower():
            print(f"{movie}, {movies[movie]['rating']}")


def exit_menu():
    """Exit the program"""
    print("Bye!")
    return False


def filter_movie(movies):
    """Filters the movies based on (minimum_rating,start_year,end_year) from user input and gives them back"""
    minimum_rating = get_movie_rating()
    start_year = get_movie_year("start")
    end_year = get_movie_year("end")
    movies_to_delete = set()
    if minimum_rating != "":
        for movie in movies:
            if minimum_rating > movies[movie]["rating"]:
                movies_to_delete.add(movie)
    if start_year != "":
        for movie in movies:
            if start_year  > movies[movie]["year"]:
                movies_to_delete.add(movie)
    if end_year != "":
        for movie in movies:
            if end_year < movies[movie]["year"]:
                movies_to_delete.add(movie)
    for movie_to_delete in movies_to_delete: #movies_copy
        del movies[movie_to_delete]
    print(movies)


def get_movie_rating():
    """Handles user input to get the rating of the new movie."""
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


def get_movie_year(text_start_end):
    """Handles user input to get the rating of the new movie."""
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


def main():
    print("********** My Movies Database **********")
    menu()


if __name__ == "__main__":
    main()





