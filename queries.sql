-- Perform one join of two tables.

SELECT *
INTO all_league
FROM american_league
UNION ALL
SELECT * FROM national_league
ORDER BY "Season"