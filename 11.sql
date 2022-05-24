SELECT title FROM movies, ratings, people, stars
WHERE stars.movie_id = movies.id AND stars.person_id = people.id AND stars.movie_id = ratings.movie_id
AND name = "Chadwick Boseman" ORDER BY rating DESC LIMIT 5;