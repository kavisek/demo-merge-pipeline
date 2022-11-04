
DROP VIEW IF EXISTS demo.latest_grade;

CREATE VIEW demo.latest_grade
AS
SELECT id, grade, last_modified, batch_uuid FROM demo.grade
ORDER BY id ASC;
