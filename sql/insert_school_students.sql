INSERT INTO
    school_students (student_id)
SELECT
    id
FROM
    users
WHERE
    first_name IS NOT NULL
    AND last_name IS NOT NULL
    AND sex IS NOT NULL
    AND age < 18
    AND country = 1
    AND city IS NOT NULL
    AND occupation = 1
    AND education = 1
    AND school_id IS NOT NULL
    AND school_city IS NOT NULL
    AND (school_grad_year >= year(curdate()) OR school_grad_year IS NULL)
    AND last_seen > '2017-03-03';