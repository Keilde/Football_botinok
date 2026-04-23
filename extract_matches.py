import requests
import psycopg2
from datetime import datetime

API_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures&quot";
HEADERS = {
    "X-RapidAPI-Key": "84e4935deemshddcbb45293698d2p194d3djsn31e7905367b8",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com
}
DB_PARAMS={
"dbname":"football_db",
"user":"postgres",
"password":"123321",
"host":"localhost"
}

def get_matches(date_str):
	querystring = {
	"date":date_str,
	"league":"135",
	"season":"2026"
	}
	response = requests.get(API_URL, headers=HEADERS, params=querystring)
	response.raise_for_status()
	return response.json()["response"]

def load_to_db(matches):
conn=psycopg2.connect(**DB_PARAMS)
cur=conn.cursor()

for m in matches:
	cur.execute("""
		Insert INTO matches (match_id, league_name, match_date, home_team, away_team,
		status, home_goals, away_goals)
		VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
		ON CONFLICT (match_id) DO UPDATE SET
			status= EXCLUDED.status,
			home_goals=EXCLUDED.home_goals,
                away_goals = EXCLUDED.away_goals;
        """, (m['fixture']['id'],
		m['league']['name'],
		m['fixture']['date'],
         	 m['teams']['home']['name'],
          	 m['teams']['away']['name'],
          	 m['fixture']['status']['short'],
           	 m['goals']['home'],
           	 m['goals']['away']
        ))
conn.commit()
cur.close()
conn.close()
print(f"Загружено {len(matches)} матчей.")

if __name__=="__main__":
	today=datetime.now().strftime('%Y-%m-%d')
	data=get_matches(today)
	if data:
		load_to_db(data)
	else:
		print("Сегодня матчей нет.")
