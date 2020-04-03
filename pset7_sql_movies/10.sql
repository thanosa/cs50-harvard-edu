SELECT DISTINCT(people.name)
FROM directors
JOIN people ON directors.person_id = people.id
WHERE directors.movie_id IN (
    SELECT movie_id
    FROM ratings
    WHERE ratings.rating >= 9);
