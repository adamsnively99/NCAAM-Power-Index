import SportsRefScraper
import csv
import Settings
from Team import Team

def loadGameFile():
    teams = {}
    with open(Settings.DATA_FOLDER + 'gamefil.csv', 'r') as gamefile:
        gamereader = csv.reader(gamefile)
        search_team = True
        for row in gamereader:
            if len(row) > 0:
                if search_team:
                    team_name = row[0]
                    new_team = Team(team_name)
                    teams[team_name] = new_team
                    search_team = False
                elif row[0] != ' Opponent':
                    new_team.addGame(float(row[3]), float(row[4]), row[0], float(row[2]))
            else:
                search_team = True
    return teams