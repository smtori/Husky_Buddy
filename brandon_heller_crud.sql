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
    WHERE student1_id = 1
    UNION
    SELECT student1_id FROM husky_match
    WHERE student2_id = 1  -- ❌ this was missing
    UNION
    SELECT 1  -- the logged in student's own photos
);

-- brandon heller #5 (2.5)
INSERT INTO match_feedback (match_id, student_id, rating, comment, created_at)
VALUES (1, 2, 4, "it was fun", NOW());

-- brandon heller #6 (2.6)
INSERT INTO student_spots (student_id, spot_id)
VALUES (1, 3);

UPDATE student_spots
SET spot_id = 2 -- new spot (Snell Library); should be a variable
WHERE student_id = 1 -- should be logged in student's id
AND spot_id = 3; -- old spot being replaced; should be a variable

DELETE FROM student_spots
WHERE student_id = 1 -- should be logged in student's id
AND spot_id = 2; -- should be a variable for the spot being removed