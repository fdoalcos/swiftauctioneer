SELECT DISTINCT(name) FROM directors, people, ratings
WHERE dictors.movie_id = ratings.movie_id AND directors.person_id = people.id
AND ratings = 9.0;