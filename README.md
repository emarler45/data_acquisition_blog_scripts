# Data Acquisition Blog Scripts

The repo contains the python code used to create and examine the dataset used in Eli Marler's blog post {name}. This repo contains three scripts: api_caller.py, assemble_data.py, and analyze_data.py.

## api_caller

This file uses the vlrdevapi package (repo here{https://github.com/Vanshbordia/vlrdevapi}) to call the vlr.gg website and get its info on professional VALORANT matches. It fetches the teams from the Americas league, their match history in the 2026 season, and roster changes of players during the 2026 season.

## assemble_data

This file uses the functions built in api_caller to collect the desired data and write them to 3 distinct csv files: matches.csv, moves.csv, and teams.csv. These can be found in the data folder.

## analyze_data

This file uses the pandas package to read in, clean, and do some EDA on the collected data. The EDA include gathering summaries on winrates, splitting team times by their iterations, and then graphing these winrates.