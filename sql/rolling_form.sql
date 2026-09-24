-- Rolling 5-match points total per team

SELECT team_name, date, pts, SUM(pts) 
OVER (
    PARTITION BY team_name ORDER BY date
    ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
) AS rolling_points
FROM matches;