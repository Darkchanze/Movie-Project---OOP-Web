import json
import movie_project

MOVIES_FILE = 'data.json'


def json_load_movies():
    """Loads the data from data.json and converts it into a dictionary via JSON."""
    with open(MOVIES_FILE, "r") as fileobj:
        movies = json.load(fileobj)
    return movies


def json_dump_movies(movies):
    """Updates the file by converting the dict into JSON."""
    with open(MOVIES_FILE, "w") as fileobj:
        fileobj.write(json.dumps(movies))


def list_movies(movies):
    """Prints all the movies with their additional data."""
    print(f"{len(movies)} movies in total:")
    for name, value in movies.items():
        print(f"{name} ({value['year']}): {value['rating']}")


def add_movie(movies):
    """Handles user input to add a new movie to the dict."""
    new_movie_name = movie_project.get_new_movie_name(movies)
    movies[new_movie_name] = {}
    new_movie_year = movie_project.get_new_movie_year()
    movies[new_movie_name]['year'] = new_movie_year
    new_movie_rating = movie_project.get_new_movie_rating()
    movies[new_movie_name]['rating'] = new_movie_rating
    print(f"Movie {new_movie_name} successfully added")
    json_dump_movies(movies)


def delete_movie(movies):
    """Handles user input to delete a movie from the dict. Matches regardless of upper and lower case letters."""
    movie_to_delete = input("Enter movie name to delete: ")
    movie_to_delete = movie_project.check_if_movie_in_list_case_insensitive(movies, movie_to_delete)
    if movie_to_delete in movies:
        del movies[movie_to_delete]
        print(f"Movie {movie_to_delete} successfully deleted")
    else:
        print(f"Movie {movie_to_delete} doesn't exist!")
    json_dump_movies(movies)


def update_movie(movies):
    """Handles user input to update a movie from the dict. Matches regardless of upper and lower case letters."""
    movie_to_update = input("Enter movie name to update: ")
    movie_to_update = movie_project.check_if_movie_in_list_case_insensitive(movies, movie_to_update)
    if movie_to_update in movies:
        new_movie_rating = movie_project.get_new_movie_rating()
        movies[movie_to_update]['rating'] = new_movie_rating
        print(f"Movie {movie_to_update} successfully updated")
    else:
        print(f"Movie {movie_to_update} doesn't exist!")
    json_dump_movies(movies)



