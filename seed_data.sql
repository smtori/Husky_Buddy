USE `husky-buddy-orig`;
-- ======================================
-- Sample Data
-- =======================================
-- User Data
INSERT INTO husky_user(`first_name`, `last_name`, `email`, `year`, `verification_status`)
VALUES('Brandon', 'Heller', 'he.bra@northeastern.edu','1st', 'verified'),
  ('Natalie', 'Frost','fro.nat@northeastern.edu', '2nd', 'verified' ),
  ('Sarah', 'Miller','miller.sa@northeastern.edu','3rd','pending');


-- Match Data
INSERT INTO husky_match(`student1_id`,`student2_id`, `status`,`matched_on`)
VALUES(1,3,'active','2026-02-10');
-- Major Data
INSERT INTO student_major_tags(`student_id`, `major_id`)
VALUES(1,26),
(1,15),
(2,56),
(2,26),
(3,26),
(3,15);


-- Interest Data
INSERT INTO student_interest(`student_id`, `interest_id`)
VALUES(1,1),
(1,6),
(2,3),
(2,6),
(3,1);


INSERT INTO campus_spot(`spot_name`,`location`)
VALUES('Marino Recreation Center','369 Huntington Ave'),
('Snell Library','360 Huntington Ave'),
('Tatte Bakery','360 Huntington Ave'),
('Prudential Center','800 Boylston St'),
('Kigo Kitchen','360 Huntington Ave');


-- =======================================
-- Additional Sample Data for Remaining Tables
-- =======================================


-- Student Spots
INSERT INTO student_spots (student_id, spot_id)
VALUES
   (1, 1), -- Brandon likes Marino Recreation Center
   (2, 2), -- Natalie likes Snell Library
   (3, 3); -- Sarah likes Tatte Bakery


-- Icebreaker Prompts
INSERT INTO icebreaker_prompt (prompt_text, category)
VALUES
   ('What is your favorite place to study on the Boston campus?', 'Campus Life'),
   ('What club, sport, or activity at Northeastern have you enjoyed the most so far?', 'Student Life'),
   ('If you could grab food anywhere near campus right now, where would you go?', 'Food');


-- Match Icebreaker
INSERT INTO match_icebreaker (match_id, prompt_id, shown_at)
VALUES
   (1, 1, '2026-02-10 12:00:00'),
   (1, 2, '2026-02-10 12:05:00'),
   (1, 3, '2026-02-10 12:10:00');


-- Student Availability
INSERT INTO student_availability (student_id, day_of_week, start_time, end_time)
VALUES
   (1, 'Monday', '14:00:00', '16:00:00'),
   (2, 'Wednesday', '11:00:00', '13:00:00'),
   (3, 'Friday', '15:30:00', '18:00:00');


-- Meetup Photo
INSERT INTO meetup_photo (match_id, uploaded_by, photo_url, caption, uploaded_at)
VALUES
   (1, 1, 'https://huskybuddy.app/photos/marino-meetup-1.jpg', 'First meetup after working out at Marino.', '2026-02-10 17:30:00'),
   (1, 3, 'https://huskybuddy.app/photos/tatte-chat-1.jpg', 'Grabbed coffee and talked about classes at Tatte.', '2026-02-10 18:15:00');


-- Match Feedback
INSERT INTO match_feedback (match_id, student_id, rating, comment, created_at)
VALUES
   (1, 1, 5, 'Great match. Easy to talk to and we had a lot in common as Northeastern students.', '2026-02-11 10:00:00'),
   (1, 3, 4, 'Really positive experience. Would love better overlap in availability next time.', '2026-02-11 10:15:00');


-- Admin
INSERT INTO admin (name, email, role)
VALUES
   ('Adam Johnson', 'johnson.ad@northeastern.edu', 'IT admin'),
   ('Johanna Park', 'park.jo@northeastern.edu', 'Data lead');


-- Flag Report
INSERT INTO flag_report (reporter_id, reported_id, reason, status, created_at)
VALUES
   (2, 3, 'Missed meetup without sending a message in advance.', 'open', '2026-03-01 09:30:00'),
   (1, 2, 'Profile information seemed incomplete and possibly misleading.', 'reviewed', '2026-03-02 14:20:00');


-- Moderation Action
INSERT INTO moderation_action (admin_id, user_id, report_id, action_type, action_date, notes)
VALUES
   (1, 3, 1, 'warning issued', '2026-03-01 12:00:00', 'Sent reminder about meetup etiquette and communication expectations.'),
   (2, 2, 2, 'under review', '2026-03-02 16:00:00', 'Reviewed reported profile and requested clarification from the user.');




