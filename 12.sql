SELECT title FROM movies, stars, people
WHERE stars.movie_id = movies.id AND stars.person_id = people.id
AND name = "Johnny Depp" OR name = "Helena Bonham Carter"; 