SELECT name FROM people JOIN stars ON stars.person_id = people.id JOIN movies ON movies.id = stars.peron_id WHERE name = "Kevin Bacon" AND birth = 1958;
