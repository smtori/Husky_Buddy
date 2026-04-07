USE `husky-buddy-orig`;

-- adam johnson #1 (1.1)
SELECT * FROM husky_user;

-- adam johnson #2 (1.2)
SELECT * FROM flag_report
INNER JOIN husky_user ON flag_report.reported_id = husky_user.student_id;

-- adam johnson #3 (1.3) FLAGGING FOR REVIEW - husky-buddy.sql update to moderation_action.action_type to enumeration required for this to work
DELETE FROM husky_user
WHERE student_id IN (
    SELECT user_id FROM moderation_action
    WHERE action_type = 'removed'
);

-- adam johnson #4 (1.4)
INSERT INTO flag_report (reporter_id, reported_id, reason, status, created_at)
VALUES (1, 2, 'cyberbullying', 'under review', NOW());


-- adam johnson #5 (1.5) NOTE: SSO auth handled at application level, not in SQL. This is the best that can be done on the SQL level
ALTER TABLE husky_user
ADD CONSTRAINT check_northeastern_email
CHECK (email LIKE '%@northeastern.edu');


-- adam johnson #6 (1.6)
SELECT
    flag_report.report_id,
    flag_report.reason,
    flag_report.created_at,
    flag_report.status,
    reporter.email AS reporter_email,
    reported.email AS reported_email
FROM flag_report
INNER JOIN husky_user AS reporter ON flag_report.reporter_id = reporter.student_id
INNER JOIN husky_user AS reported ON flag_report.reported_id = reported.student_id
WHERE flag_report.status = 'pending'
ORDER BY flag_report.created_at ASC;