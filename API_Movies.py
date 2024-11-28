from API_Key import KEY
import requests
import json


def api_request_data(title):
    """Used API https://www.omdbapi.com/"""

    title_request = "&t=" + "+".join(title.split(" "))
    api_response = requests.get(f"http://www.omdbapi.com/?apikey={KEY}{title_request}")
    movie_infos = api_response.json()
    title = movie_infos["Title"]
    year = movie_infos["Year"]
    rating = movie_infos["Ratings"][0]["Value"]
    poster_url = movie_infos["Poster"]
    return title, year, rating, poster_url








