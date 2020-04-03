SELECT DISTINCT(people.name) AS starName
FROM stars s1
JOIN stars s2 ON s1.movie_ID = s2.movie_ID
JOIN people ON s2.person_id = people.id
WHERE s1.person_id = (
    SELECT DISTINCT(stars.person_id)
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958)
AND s2.person_id != (
    SELECT DISTINCT(stars.person_id)
    FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958);