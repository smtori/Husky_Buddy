USE `husky-buddy-orig`;

-- adam johnson #1 (1.1)
SELECT * FROM husky_user;

-- adam johnson #2 (1.2)
SELECT * FROM flag_report
LEFT JOIN husky_user ON flag_report.reported_id = husky_user.student_id;

-- adam johnson #3 (1.3)
