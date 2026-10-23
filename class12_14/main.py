from fastapi import FastAPI, Query
from src import MovieInput, MovieResponse
import logging

app = FastAPI(title="Movie API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): 
    #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}

@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    #Converts the model to a Python dictionary.
    return movie.model_dump() 

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record

@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    # TODO 1: return up to limit movies as a list.
    # Log the number returned at INFO.
    # hint: movies is a dictionary whose values are movie records.
    result = list(movies.values())[:limit]
    logger.info(f"Returning {len(result)} movies")
    return result

@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    # TODO 2: 
    # Convert movie to a dictionary, add the new ID, and store it.
    # Log the new ID at INFO and return the stored record.
    new_id = max(movies, default = 0) + 1
    record = movie.model_dump()
    record["id"] = new_id
    movies[new_id] = record
    logger.info(f"Added movie with id {new_id}")
    return record