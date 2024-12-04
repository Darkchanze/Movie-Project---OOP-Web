import statistics



string_list = ['7.9/10', '6.5/10', '8.0/10', '9.0/10', '8.4/10', '8.4/10', '6.1/10']
float_list = [float(rating.split("/")[0]) for rating in string_list]
print(float_list)
#print(f"Average rating: {round(statistics.mean(list), 1)}")
#print(f"Median rating: {round(statistics.median(list), 1)}")


# list_of_ratings = [movie['rating'] for movie in movies.values()]