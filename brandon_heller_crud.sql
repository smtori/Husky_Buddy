USE `husky-buddy-orig`;

-- brandon heller #1 (2.1) NOTE: will be from the standpoint of inserting brandon's prompt to DB
INSERT INTO icebreaker_prompt (prompt_text, category)
VALUES ("I like pizza", "Favorite Food")

-- brandon heller #2 (2.2)
SELECT match1.first_name AS your_name,
       match1.last_name AS your_lastName,
       match1.email AS your_email,
       match2.first_name as match_name,
       match2.last_name AS match_lastName,
       match2.email AS match_email
FROM husky_match
INNER JOIN husky_user AS match1 ON match1.student_id = student1_id
INNER JOIN husky_user AS match2 ON match2.student_id = student2_id
WHERE husky_match.student1_id = 1; -- should be the logged in students id

-- brandon heller #3 (2.3) NOTE - we should rewrite student_availability to be more query friendly
UPDATE student_availability
SET day_of_week = 'Friday', start_time = NOW()
WHERE student_id = 1 -- should be variable of current student
AND day_of_week = 'Monday';

-- brandon heller #4 (2.4) NOTE - we should rename uploaded_by to uploader_id for query simplicity
SELECT photo_url FROM meetup_photo
WHERE uploaded_by IN (
    SELECT student2_id FROM husky_match
    WHERE student1_id = 1 -- should be the logged in student's id
    UNION
    SELECT husky_match.student1_id
);

-- brandon heller #5 (2.5)
INSERT INTO match_feedback (match_id, student_id, rating, comment, created_at)
VALUES (1, 1, 4, "it was fun", NOW());

-- brandon heller #6 (2.6)
-- we have to rewrite interest_tag, it's implementation doesn't match the ER diagram