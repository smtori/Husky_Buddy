DROP DATABASE IF EXISTS `husky-buddy-orig`;
CREATE DATABASE `husky-buddy-orig`;
USE `husky-buddy-orig`;

CREATE TABLE IF NOT EXISTS husky_user (
   student_id INT NOT NULL AUTO_INCREMENT,
   firstName varchar(50) NOT NULL,
   lastName varchar(50) NOT NULL,
   nu_email varchar(75) NOT NULL,
   class_year ENUM('1st', '2nd', '3rd', '4th', '5th', 'Grad') NOT NULL,
   verification_status varchar(20),
   PRIMARY KEY (student_id),
   UNIQUE INDEX (nu_email)

);
-- Husky Matching Ids
CREATE TABLE IF NOT EXISTS husky_match (
    match_id INT NOT NULL AUTO_INCREMENT,
    student1_id INT NOT NULL,
    student2_id INT NOT NULL,
    status varchar(20),
    matched_on datetime NOT NULL,
    PRIMARY KEY (match_id),
    FOREIGN KEY (student1_id) REFERENCES husky_user(student_id),
    FOREIGN KEY (student2_id) REFERENCES husky_user(student_id),
    UNIQUE INDEX (match_id),
    UNIQUE INDEX unique_pair (student1_id, student2_id)
);
-- Student Interest Tags
CREATE TABLE IF NOT EXISTS interest_tag(
    tag_id   INT NOT NULL AUTO_INCREMENT,
    tag_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (tag_id)
);
-- Student Interests
CREATE TABLE IF NOT EXISTS student_interest(
    student_id  INT NOT NULL,
    interest_id INT NOT NULL,
    PRIMARY KEY (student_id, interest_id),
    FOREIGN KEY (student_id) REFERENCES husky_user(student_id) ON DELETE CASCADE,
    FOREIGN KEY (interest_id) REFERENCES interest_tag(tag_id) ON DELETE CASCADE
);
-- Majors
CREATE TABLE majors (
    major_id INT AUTO_INCREMENT,
    major_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY(major_id)
);
-- Major Tags
CREATE TABLE student_major_tags(
    student_id INT NOT NULL,
    major_id INT NOT NULL,
    PRIMARY KEY (student_id, major_id),
    FOREIGN KEY (student_id) REFERENCES husky_user(student_id) ON DELETE CASCADE,
    FOREIGN KEY (major_id) REFERENCES majors(major_id) ON DELETE CASCADE
);

-- Campus Spot
CREATE TABLE campus_spot(
    spot_id INT NOT NULL AUTO_INCREMENT,
    spot_name varchar(100),
    location varchar(100),
    PRIMARY KEY (spot_id)
);

-- Student Spots
CREATE TABLE student_spots(
    student_id INT NOT NULL,
    spot_id INT NOT NULL,
    PRIMARY KEY (student_id, spot_id),
    FOREIGN KEY (student_id) REFERENCES husky_user(student_id) ON DELETE CASCADE,
    FOREIGN KEY (spot_id) REFERENCES campus_spot(spot_id) ON DELETE CASCADE
);

-- icebreaker prompt
CREATE TABLE IF NOT EXISTS icebreaker_prompt (
    prompt_id INT NOT NULL AUTO_INCREMENT,
    prompt_text TEXT NOT NULL,
    category VARCHAR(50),
    PRIMARY KEY (prompt_id)
);

-- match icebreaker
CREATE TABLE IF NOT EXISTS match_icebreaker (
    match_id INT NOT NULL,
    prompt_id INT NOT NULL,
    shown_at DATETIME DEFAULT NOW(),
    PRIMARY KEY (match_id, prompt_id),
    FOREIGN KEY (match_id) REFERENCES husky_match(match_id) ON DELETE CASCADE,
    FOREIGN KEY (prompt_id) REFERENCES icebreaker_prompt(prompt_id) ON DELETE CASCADE
);

-- student availability
CREATE TABLE IF NOT EXISTS student_availability (
    availability_id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    day_of_week ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    PRIMARY KEY (availability_id),
    FOREIGN KEY (student_id) REFERENCES husky_user(student_id) ON DELETE CASCADE,
    UNIQUE INDEX unique_slot (student_id, day_of_week, start_time, end_time)
);

-- meetup photo
CREATE TABLE IF NOT EXISTS meetup_photo (
    photo_id INT NOT NULL AUTO_INCREMENT,
    match_id INT NOT NULL,
    uploaded_by INT NOT NULL,
    photo_url VARCHAR(255) NOT NULL,
    caption TEXT,
    uploaded_at DATETIME DEFAULT NOW(),
    PRIMARY KEY (photo_id),
    FOREIGN KEY (match_id) REFERENCES husky_match(match_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES husky_user(student_id) ON DELETE CASCADE
);

-- match feedback
CREATE TABLE IF NOT EXISTS match_feedback (
    feedback_id INT NOT NULL AUTO_INCREMENT,
    match_id INT NOT NULL,
    student_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME DEFAULT NOW(),
    PRIMARY KEY (feedback_id),
    FOREIGN KEY (match_id) REFERENCES husky_match(match_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES husky_user(student_id) ON DELETE CASCADE,
    UNIQUE INDEX one_review_per_match (match_id, student_id)
);

-- admin
CREATE TABLE admin(
    admin_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    admin_email VARCHAR(100) NOT NULL,
    role VARCHAR(100) NOT NULL,
    status VARCHAR(100) NOT NULL,
    PRIMARY KEY(admin_id)
);
-- create report
CREATE TABLE IF NOT EXISTS flag_report(
    report_id INT NOT NULL AUTO_INCREMENT,
    reporter_id INT NOT NULL,
    reported_id INT NOT NULL,
    reason text,
    status varchar(20),
    created_at DATETIME,
    PRIMARY KEY (report_id),
    FOREIGN KEY (reporter_id) REFERENCES husky_user(student_id),
    FOREIGN KEY (reported_id) REFERENCES husky_user(student_id)
);


-- moderation action
CREATE TABLE moderation_action(
    action_id INT AUTO_INCREMENT,
    admin_id INT,
    user_id INT,
    report_id INT,
    action_type VARCHAR(100),
    action_date TIMESTAMP,
    notes TEXT,
    PRIMARY KEY (action_id),
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    FOREIGN KEY (user_id) REFERENCES husky_user(student_id),
    FOREIGN KEY (report_id) REFERENCES flag_report(report_id)
);
-- ==================================================
-- Add in Northeastern majors for the dropdown
INSERT INTO majors (major_name) VALUES
    ('Africana Studies'),
    ('American Sign Language-English Interpreting'),
    ('Advanced Manufacturing Systems'),
    ('Analytics'),
    ('Applied Physics'),
    ('Architectural Studies'),
    ('Architecture'),
    ('Art'),
    ('Behavioral Neuroscience'),
    ('Biochemistry'),
    ('Bioengineering'),
    ('Biology'),
    ('Biomedical Physics'),
    ('Biotechnology'),
    ('Business Administration'),
    ('Cell and Molecular Biology'),
    ('Chemical Engineering'),
    ('Chemistry'),
    ('Civil Engineering'),
    ('Communication and Media Studies'),
    ('Communication Studies'),
    ('Computer Engineering'),
    ('Computer Science'),
    ('Cultural Anthropology'),
    ('Cybersecurity'),
    ('Data Science'),
    ('Design'),
    ('Digital Communication and Media'),
    ('Ecology and Evolutionary Biology'),
    ('Economics'),
    ('Electrical and Computer Engineering'),
    ('Electrical Engineering'),
    ('English'),
    ('Environmental and Sustainability Sciences'),
    ('Environmental Engineering'),
    ('Environmental Studies'),
    ('Finance and Accounting Management'),
    ('Game Art and Animation'),
    ('Game Design'),
    ('Global Asian Studies'),
    ('Health Science'),
    ('Healthcare Administration'),
    ('History'),
    ('History Culture and Law'),
    ('Human Services'),
    ('Industrial Engineering'),
    ('Information Technology'),
    ('Interdisciplinary Studies'),
    ('International Affairs'),
    ('International Business'),
    ('Journalism'),
    ('Landscape Architecture'),
    ('Linguistics'),
    ('Management'),
    ('Marine Biology'),
    ('Mathematics'),
    ('Mechanical Engineering'),
    ('Mechatronics'),
    ('Media and Screen Studies'),
    ('Media Arts'),
    ('Music'),
    ('Nursing'),
    ('Performance and Extended Realities'),
    ('Pharmaceutical Sciences'),
    ('Pharmacy Studies'),
    ('Philosophy'),
    ('Physics'),
    ('Political Science'),
    ('Politics Philosophy and Economics'),
    ('Project Management'),
    ('Psychology'),
    ('Public Health'),
    ('Public Relations'),
    ('Religious Studies'),
    ('Sociology'),
    ('Spanish'),
    ('Speech-Language Pathology and Audiology'),
    ('Studio Art'),
    ('Theatre'),
    ('Undeclared');

INSERT INTO interest_tag (tag_name) VALUES
    ('Sports and Fitness'),
    ('Arts and Creativity'),
    ('Tech'),
    ('Gaming'),
    ('Food and Social'),
    ('Careers and Academic'),
    ('Entertainment and Culture'),
    ('Wellness and Lifestyle');

-- =======================================
-- Sample Data
-- =======================================
-- User Data
INSERT INTO husky_user(`firstName`, `lastName`, `nu_email`, `class_year`, `verification_status`)
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