-- summary (materialized-view-like) refresh
DROP TABLE IF EXISTS summary_school_year;
CREATE TABLE summary_school_year AS
SELECT
  a.year,
  s.school_id,
  e.subgroup_code,
  AVG(CASE WHEN a.subject='ELA'  THEN a.qual_rate END)  AS ela_rate,
  AVG(CASE WHEN a.subject='MATH' THEN a.qual_rate END)  AS math_rate,
  t.chronic_absent_rate
FROM assessments a
JOIN attendance t
  ON t.year=a.year AND t.school_id=a.school_id AND t.subgroup_code=a.subgroup_code
JOIN enrollment e
  ON e.year=a.year AND e.school_id=a.school_id AND e.subgroup_code=a.subgroup_code
JOIN school s
  ON s.school_id=a.school_id
GROUP BY a.year, s.school_id, e.subgroup_code;
