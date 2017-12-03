INSERT INTO
    university_students (student_id)
SELECT
    id
FROM
    users
WHERE
    first_name IS NOT NULL
    AND last_name IS NOT NULL
    AND sex IS NOT NULL
    AND age BETWEEN 18 AND 24
    AND country = 1
    AND city IS NOT NULL
    AND occupation = 2
    AND education = 3
    AND university_id IS NOT NULL
    AND university_faculty IS NOT NULL
    AND university_city IS NOT NULL
    AND (university_grad_year >= year(curdate()) OR university_grad_year IS NULL)
    AND last_seen > '2017-03-03';