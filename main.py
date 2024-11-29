from storage.storage_csv import StorageCsv
from movie_app.movie_app import MovieApp

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