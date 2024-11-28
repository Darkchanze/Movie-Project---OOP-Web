def generate_website(movies_data: dict):
    """
    Generate an HTML file for the movie website based on movie_data.

    This function creates the movie grid HTML, updates a base HTML template.
    Both are put into the old html and saved in a new html file.

    Args:
        movies_data (dict): A dictionary containing the movie details. Each key is the movie name,
                                and its value is another dictionary with "year" and "poster_url" "ratings" keys.
    """
    html_code_movie_grid = create_html_code_for_website(movies_data)
    html_code_title = "The movie app"
    base_html = open_base_html()
    updated_html = base_html.replace("__TEMPLATE_MOVIE_GRID__", html_code_movie_grid)
    final_html = updated_html.replace("__TEMPLATE_TITLE__", html_code_title)
    save_final_html_in_document(final_html)


def create_html_code_for_website(movies_data: dict):
    """
    Creates the HTML code for the grid of the html.

    This function generates an HTML list of movie cards based on the provided movie data.
    Each movie card includes the poster image, title, and release year.

    Args:
        movies_data (dict): A dictionary containing the movie details. Each key is the movie name,
                                and its value is another dictionary with "year" and "poster_url" "ratings" keys.
    Returns:
        str: An HTML string representing the movie grid.
    """
    html_code = ""
    for movie in movies_data:
        movie_name = movie
        movie_year = movies_data[movie]["year"]
        movie_poster = movies_data[movie]["poster_url"]
        #movie_rating = movies_data[movie]["rating"]             #Get rating if later added
        html_code += (f'''
        <li>
            <div class="movie">
                <img class="movie-poster" src="{movie_poster}" alt="Poster {movie_name}">
                <div class="movie-title">{movie_name}</div>
                <div class="movie-year">{movie_year}</div>
            </div>
        </li>
        ''')
    return html_code

def open_base_html():
    """
    Opens and reads the base HTML template file.

    This function reads the contents of "index_template.html", which serves as the base
    structure for the movie website. If an error occurs, an appropriate message is printed.

    Returns:
        str: The content of the base HTML template as a string.
    """
    try:
        with open("index_template.html", "r") as handle:
            base_html = handle.read()
            return base_html
    except FileNotFoundError:
        print("The file 'index_template.html' was not found.")
    except IOError:
        print("There was an issue opening the file.")


def save_final_html_in_document(final_html: str):
    """
    Saves the final HTML code to a file.

    This function writes the provided HTML string to a file named "index.html".
    If an error occurs, an appropriate message is printed.

    Args:
        final_html (str): The HTML content to be saved.
    """
    try:
        with open("index.html", "w") as handle:
            handle.write(final_html)
    except PermissionError:
        print("You do not have permission to write to this file.")
    except IOError:
        print("There was an issue saving the file.")