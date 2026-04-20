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
"password":"123",
"host":"localhost"
}

def get_matches(date_str):
	querystring = {
	"date":date_str,
	"league":"135"
	"season":"2026"
	}
	response = request.get(API_URL,headers=HEADERS, params=querystring)
	response.raise_for_status()
	return response.json()["response"]

def load_to_bd(matches):
conn=psycopg2.connect(**DB_PARAMS)
cur=conn.cursor()
