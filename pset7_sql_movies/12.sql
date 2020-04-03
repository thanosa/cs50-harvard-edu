SELECT movies.title
FROM (
    SELECT stars.movie_id
    FROM STARS
    WHERE person_id IN (
        SELECT DISTINCT(stars.person_id)
        FROM stars
        JOIN people ON stars.person_id = people.id
        WHERE people.name = 'Helena Bonham Carter')) as temp
JOIN movies ON movies.id = temp.movie_id
WHERE temp.movie_id IN (
    SELECT stars.movie_id
    FROM STARS
    WHERE person_id IN (
        SELECT DISTINCT(stars.person_id)
        FROM stars
        JOIN people ON stars.person_id = people.id
        WHERE people.name = 'Johnny Depp'));


