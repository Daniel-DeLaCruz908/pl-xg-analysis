-- Season-long xG performance per team ranked by overperformance to underperformance

SELECT team_name, SUM(scored) - SUM(xG) AS performance, SUM(pts) AS total_points
FROM matches
GROUP BY team_name
ORDER BY performance DESC;