/*
List all movies with an average rating of at least 4.0.
*/
-- QUERY: movies_avg_rating
SELECT m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON r.movieId = m.movieId
GROUP BY m.movieId, m.title
HAVING AVG(r.rating) >= 4.0;

-- QUERY: most_active_users
SELECT r.userId,
       COUNT(*) AS num_ratings
FROM ratings r
GROUP BY r.userId
ORDER BY num_ratings DESC, r.userId ASC
LIMIT 3;

-- QUERY: genre_count
WITH RECURSIVE
split AS (
  SELECT movieId, genres || '|' AS rest
  FROM movies
  UNION ALL
  SELECT movieId, substr(rest, instr(rest, '|') + 1)
  FROM split
  WHERE rest <> ''
),
genres AS (
  SELECT movieId, substr(rest, 1, instr(rest, '|') - 1) AS genre
  FROM split
  WHERE instr(rest, '|') > 0
)
SELECT genre AS genre_name,
       COUNT(DISTINCT movieId) AS distinct_movies
FROM genres
WHERE genre NOT IN ('', '(no genres listed)')
GROUP BY genre
ORDER BY distinct_movies DESC, genre_name ASC;

-- QUERY: most_common_rating
SELECT rating,
       COUNT(*) AS rating_count
FROM ratings
GROUP BY rating
ORDER BY rating_count DESC, rating DESC
LIMIT 1;
