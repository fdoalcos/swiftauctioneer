SELECT DISTINCT(name) FROM people, stars, movies
WHERE stars.movie_id = movies.id AND stars.person_id = people.id
AND year = 2004 ORDER BY birth;