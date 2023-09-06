from app.models import Movie
import csv


def run():
     with open("movies.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Movie.objects.get_or_create(
                movieId=row[0],
                title=row[1],
                genres=row[2],
                )