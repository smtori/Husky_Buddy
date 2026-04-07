USE `husky-buddy-orig`;

-- natalie frost #1 (3.1)
UPDATE student_major_tags
SET major_id = (
    SELECT major_id FROM majors
    WHERE major_name = 'Computer Science'
)
WHERE student_id = 123456;

-- natalie frost #2 (3.2)
DELETE FROM student_interest
WHERE interest_id = (
    SELECT tag_id FROM interest_tag
    WHERE tag_type = 'Tennis'
);

-- natalie frost #3 (3.3)
ALTER TABLE husky_user
ADD CONSTRAINT check_northeastern_email
CHECK (email LIKE '%@northeastern.edu');


-- natalie frost #4 (3.4)
SELECT first_name, last_name from husky_user
INNER JOIN husky_match ON husky_match.student2_id = husky_user.student_id
WHERE husky_user.student_id = 1; -- should be logged in user


-- natalie frost #5 (3.5)
INSERT INTO flag_report (reporter_id, reported_id, reason, status, created_at)
VALUES (1, 2, 'uncomfortable interaction during coffee chat', 'under review', NOW());
DELETE FROM husky_match
WHERE (student1_id = 1 AND student2_id = 2)
OR (student2_id = 1 AND student1_id =2 );


-- natalie frost #6 (3.6)
INSERT INTO student_interest (student_id, interest_id)
VALUES
    (123456, 1),
    (123456, 2),
    (123456, 3),
    (123456, 4);

INSERT INTO interest_tag (tag_type)
VALUES
    ('football'),
    ('golf'),
    ('running'),
    ('fortnite');