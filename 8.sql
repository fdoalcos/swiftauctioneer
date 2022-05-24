SELECT name FROM people, stars, movies
WHERE stars.movie_id = stars.movies.id AND stars.person_id = people.id
AND title = "Toy Story";