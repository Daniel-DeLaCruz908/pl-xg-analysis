-- Individual losses where a team generated high xG but still lost

SELECT team_name, date, scored, xG, scored - xG AS match_performance
FROM matches
WHERE result = 'l'
ORDER BY xG DESC;