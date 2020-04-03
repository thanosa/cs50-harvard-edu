SELECT movies.title
FROM stars
JOIN movies ON movies.id = stars.movie_id
JOIN ratings ON movies.id = ratings.movie_id
WHERE person_id IN (
    SELECT DISTINCT(stars.person_id)
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Chadwick Boseman')
ORDER BY ratings.rating DESC
LIMIT 5;