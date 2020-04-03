SELECT s1.movie_id AS movie1, s2.movie_id AS movie2, s1.person_id AS star1, s2.person_id AS star2
FROM stars s1
JOIN stars s2 ON s1.movie_ID = s2.movie_ID
WHERE s1.person_id = (
    SELECT DISTINCT(stars.person_id)
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Johnny Depp')

    AND s2.person_id = (

    SELECT DISTINCT(stars.person_id)
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Helena Bonham Carter');