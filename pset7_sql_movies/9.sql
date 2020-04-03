SELECT people.name
FROM people
WHERE people.id IN (
    SELECT DISTINCT(stars.person_id)
    FROM movies
    JOIN stars ON movies.id = stars.movie_id
    WHERE year = 2004)
ORDER BY people.birth;