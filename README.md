# Premier League Standings Data Pipeline (Python + SQL) 

## OVerview 
This project builds a simple data pipelie that retrieves English Premier League standings from an external API, processes the data using Python, and stores it in a Microsoft SQL server database for fast access and analytics. 

## Problem Statement 
On matchdays, users experience delays when trying to view updated league standings due to slow external websites. This project addresses that issue by creating a local, fast-access data pipeline that ensures timely and reliable standings data. 

## Objective
-  Provide near real-time league standings
-  Reduce latency in accessing standings
-  Enable structured data storage for analytics and reporting

## Tools & Technologies
-  Python
-  Microsoft SQL Server
-  Rest API(API-Football)

## Data Pipeline Architecture 
1. Extract
   - Fetch data from API
   -  Authenticate using API key stored in .env
2. Transform
   - Parse JSON response
   - Clean and structure data using pandas
  
3. Load
   -  Connect to SQL Server
   -  Insert/Upsert cleaned into database

## Data Model  
Fields Captured;
-  Season
-  Position
-  Team ID
-  Team ID
-  Matches Played
-  Wins / Draws / Losses
-  Goals For/Against
-  Goal Difference
-  Points
-  Recent Form

## Data Quality Checks
-  Ensure exactly 20 teams
-  No missing values
-  Correct data types (integers for numeric fields)

## Approach & Though Process 
- Broke down the problem into Extract, Transform, Load stages
- Focused on minimal viable pipeline first, then improved reliability
- Used environment variables to secure credentials
- Debugged issues iteratively (API response, environment setup, SQL connection)

## Key Learnings 
- API data extraction and handlign JSON
- Data cleaning and transformation with Python
- Connecting Python to SQL Server
- Writing efficient insert/upsert logic
- Debugging and troubleshooting environment issues
- Structuring projects for scalability

## Project Structure 
- test.ipynb
- .env
- .gitignore
- README.md

## Future improvements 
- Automate Pipeline (Scheduling)
- Add Dashboard (PowerBI)
- Improve error handling and logging

