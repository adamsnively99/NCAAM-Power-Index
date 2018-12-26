import SportsRefScraper
import csv
from Team import Team

teams = {}
with open('gamefile.csv', 'r') as gamefile:
    gamereader = csv.reader(gamefile)
    search_team = True
    for row in gamereader:
        print(row)
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

print(teams)

updatePage = SportsRefScraper.getGameIndexPage(11, 23, 2018)
SportsRefScraper.scrapeIndexPage(updatePage, teams)
SportsRefScraper.updateDefensiveRatings(teams)
SportsRefScraper.updateAdjustedOffensiveRatings(teams)
SportsRefScraper.writeTeamData(teams)
SportsRefScraper.writeGameData(teams)