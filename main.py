
import os  #--->  Talking to our operating system. Allows you to be able to read and write different types of files in your system.
import json #---> API response in going to be in JSON format, the JSON library helps us handle all that. 
import requests # ---> Allows us send request to the API. 
import pandas as pd  # ---> The pandas library helps in pandas and performing data transformations in tables(DataFrames, Python)
import pyodbc as connector # ---> Allows to connect to mssql programmatically. All the manual that could be done in mssql server is done here in with python. Load data from python via the pyodbc library
from dotenv import load_dotenv  #---> Allows us to load secrets from a dotenv file, safely. 

def extract():
    load_dotenv()

    API_KEY = os.getenv("API_KEY") # Get the API Key
    API_HOST = os.getenv("API_HOST") # Get the APi Host 
    SEASON = os.getenv("SEASON") # Specifies the season
    LEAGUE_ID = os.getenv("LEAGUE_ID")

    url = "https://v3.football.api-sports.io/standings"


    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    querystring = {
        "league": LEAGUE_ID,
        "season": SEASON 
    }

    response = requests.get(url=url,
                        headers=headers,
                        params=querystring
                        )
    return response.json()

def transform(payload):
    standing_list = payload['response'][0]['league']['standings'][0]

    rows = []
    column_names = ['season', 'position', 'team_id', 'team', 'played', 'won', 'draw', 'lost', 'goals_for', 'goals_against', 'goal_diff', 'points', 'form' ]

    #Loop through the list and extract the needed fields.
    for club in standing_list:
        record = (
                    2024,
                    club['rank'],
                    club['team']['id'],
                    club['team']['name'],
                    club['all']['played'],
                    club['all']['win'],
                    club['all']['draw'],
                    club['all']['lose'],
                    club['all']['goals']['for'],
                    club['all']['goals']['against'],
                    club['goalsDiff'],
                    club['points'],
                    club['form']
        )

        # Append this tuple to the empty rows list variable
        rows.append(record)

    if len(rows) !=20:
        raise ValueError("Data quality check failed: Expected 20 teams")
    
    return rows


def load (rows):

    db_connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=gideon-oquongud\SQLEXPRESS;"
        "DATABASE=premier_league_standing;"
        "Trusted_Connection=yes;"
    )
    
    # Initialize cursor for executing SQL commands
    cursor = db_connection.cursor()

    # Validate target table existence before performing any load operation
    sql_table = 'standings'

    cursor.execute("""
            SELECT 1 
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = ?
                """, (sql_table,))

    if cursor.fetchone() is None:
        raise SystemExit(f"This table '{sql_table}' is NOT found...please create it...")
    else: 
        print(f"[SUCCESS] - This table '{sql_table}' exist! Continue to the next phase!")
    
    # Define UPSERT (MERGE) logic: update existing records or insert new ones based on business key
    
    merge_SQL = f"""
        MERGE INTO {sql_table} AS target
        USING (VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source
        (season, position, team_id, team, played, won, draw, lost, goals_for, goals_against, goal_diff, points, form)

        ON target.team_id = source.team_id AND target.season = source.season

        WHEN MATCHED THEN 
            UPDATE SET 
                position        = source.position,
                team            = source.team,
                played          = source.played, 
                won             = source.won,
                draw            = source.draw, 
                lost            = source.lost, 
                goals_for       = source.goals_for, 
                goals_against   = source.goals_against, 
                goal_diff       = source.goal_diff, 
                points          = source.points,
                form            = source.form
        WHEN NOT MATCHED THEN 
        INSERT (season, position, team_id, team, played, won, draw, lost,goals_for, goals_against, goal_diff, points, form)
        VALUES(source.season, source.position, source.team_id, source.team, source.played, source.won, source.draw, source.lost, source.goals_for, source.goals_against, source.goal_diff, source.points, source.form);
        """
    
    try:
        cursor.executemany(merge_SQL, rows)
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        raise e
    finally:
        cursor.close()
        db_connection.close()


def main():
    payload = extract()
    rows = transform(payload)
    load(rows)

if __name__ == "__main__":
    main()