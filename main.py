from storage_json import StorageJson
from movie_app import MovieApp
from storage_csv import StorageCsv

def main():
    """Main program sequence of movie project."""
    #storage = StorageJson('movies.json')
    #movie_app = MovieApp(storage)
    #movie_app.run()
    storage = StorageCsv('movies.csv')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()