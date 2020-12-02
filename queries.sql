-- This query gets all the info on the most recent teams. 
WITH ordered_metrics AS (
                  SELECT s.*, ROW_NUMBER() OVER (PARTITION BY teamID ORDER BY date DESC) AS sl
                  FROM fbsprod.team_metrics AS s
                )
                SELECT * FROM ordered_metrics WHERE sl = 1;