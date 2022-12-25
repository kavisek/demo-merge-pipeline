
DROP VIEW IF EXISTS public.latest_grade;

CREATE VIEW public.latest_grade
AS
SELECT id, grade, last_modified, batch_uuid FROM public.grade
ORDER BY id ASC;
