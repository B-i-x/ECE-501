/*
List all movies with an average rating of at least 4.0.
*/
-- movies_with_min_rating.sql
SELECT m.title
FROM movies m
JOIN ratings r ON r.movieId = m.movieId
HAVING AVG(r.rating) >= 4.0;
