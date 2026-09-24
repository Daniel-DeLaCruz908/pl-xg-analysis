import requests 
import pandas as pd
import json
import sqlite3
from bs4 import BeautifulSoup

headers = {
    "Referer": "https://understat.com/league/EPL/2023",
    "X-Requested-With": "XMLHttpRequest"
}

response = requests.get("https://understat.com/getLeagueData/EPL/2023", headers=headers)

data = json.loads(response.text)

rows = []
for team_id, team_info in data["teams"].items():
    team_name = team_info["title"]
    for match in team_info["history"]:
        match["team_id"] = team_id
        match["team_name"] = team_name
        rows.append(match)

df = pd.DataFrame(rows)
df = df.drop(columns=["ppda", "ppda_allowed"])

conn = sqlite3.connect('data/epl_2023.db')

df.to_sql('matches', conn, if_exists='replace', index=False)

cursor = conn.cursor()
cursor.execute("SELECT team_name, SUM(scored) - SUM(xG) AS performance FROM matches GROUP BY team_name ORDER BY performance DESC")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("PRAGMA table_info(matches)")
for col in cursor.fetchall():
    print(col)

cursor.execute("SELECT team_name, date, pts, SUM(pts) OVER (PARTITION BY team_name ORDER BY date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_points FROM matches")
rolling_points = cursor.fetchall()
for row in rolling_points:
    print(row)

cursor.execute("SELECT team_name, date, scored, xG, scored - xG AS match_performance FROM matches WHERE result = 'l' ORDER by xG DESC")
match_performance = cursor.fetchall()
for row in match_performance:
    print(row)