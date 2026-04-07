USE `husky-buddy-orig`;

-- johanna park #1 (4.1)
SELECT
    (SELECT COUNT(*) FROM husky_user) AS total_users,
    (SELECT COUNT(*) FROM husky_user WHERE verification_status = 'verified') AS verified_users,
    (SELECT COUNT(*) FROM husky_match) AS total_matches,
    (SELECT COUNT(*) FROM husky_match WHERE status = 'active') AS active_matches;

-- johanna park #2 (4.2)
SELECT
    AVG(rating) AS avg_satisfaction,
    COUNT(*) AS total_responses,
    MIN(rating) AS lowest_rating,
    MAX(rating) AS highest_rating
FROM match_feedback;

-- johanna park #3 (4.3)
SELECT
    husky_user.year,
    majors.major_name,
    interest_tag.tag_type,
    COUNT(*) AS user_count
FROM husky_user
INNER JOIN student_major_tags ON husky_user.student_id = student_major_tags.student_id
INNER JOIN majors ON student_major_tags.major_id = majors.major_id
INNER JOIN student_interest ON husky_user.student_id = student_interest.student_id
INNER JOIN interest_tag ON student_interest.interest_id = interest_tag.tag_id
GROUP BY husky_user.year, majors.major_name, interest_tag.tag_type
ORDER BY user_count DESC;

-- johanna park #4 (4.4)
SELECT
    COUNT(DISTINCT husky_match.match_id) AS matches_met_in_person,
    COUNT(DISTINCT husky_match.match_id) * 100.0 /
        (SELECT COUNT(*) FROM husky_match) AS success_rate_percent
FROM husky_match
INNER JOIN meetup_photo ON meetup_photo.match_id = husky_match.match_id;

-- johanna park #5 (4.5)
SELECT
    YEAR(matched_on) AS year,
    MONTH(matched_on) AS month,
    COUNT(*) AS new_matches
FROM husky_match
GROUP BY YEAR(matched_on), MONTH(matched_on)
ORDER BY year ASC, month ASC;

-- johanna park #6 (4.6)
SELECT
    m1.major_name AS student1_major,
    m2.major_name AS student2_major,
    COUNT(*) AS total_matches,
    AVG(mf.rating) AS avg_satisfaction
FROM husky_match
INNER JOIN student_major_tags AS sm1 ON husky_match.student1_id = sm1.student_id
INNER JOIN student_major_tags AS sm2 ON husky_match.student2_id = sm2.student_id
INNER JOIN majors AS m1 ON sm1.major_id = m1.major_id
INNER JOIN majors AS m2 ON sm2.major_id = m2.major_id
LEFT JOIN match_feedback AS mf ON husky_match.match_id = mf.match_id
GROUP BY m1.major_name, m2.major_name
ORDER BY avg_satisfaction DESC;