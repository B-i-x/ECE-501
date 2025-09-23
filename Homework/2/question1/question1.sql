/*
List all movies with an average rating of at least 4.0.
*/
-- QUERY: movies_avg_rating
SELECT m.title, AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r ON r.movieId = m.movieId
GROUP BY m.movieId, m.title
HAVING AVG(r.rating) >= 4.0;