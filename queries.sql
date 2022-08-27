-- Perform one join of two tables.

SELECT *
INTO all_league
FROM "AL"
UNION ALL
SELECT * FROM "NL"
ORDER BY "Season"