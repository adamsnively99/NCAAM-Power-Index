import SportsRefScraper
import csv
import Settings
from Team import Team

def loadTeamsFromBoxScores():
    teams = {}
    with open('boxscoredata.csv', 'r') as datafile:
        reader = csv.reader(datafile)
        lines = datafile.readlines()
        data = []
        for line in lines:
            data.append(line.split(','))
        for i in range(0, len(data), 2):
            team_a_name = data[i][0]
            team_b_name = data[i + 1][0]
            if team_a_name not in teams:
                team_a = Team(team_a_name)
                teams[team_a_name] = team_a
            else:
                team_a = teams[team_a_name]
            if team_b_name not in teams:
                team_b = Team(team_b_name)
                teams[team_b_name] = team_b
            else:
                team_b = teams[team_b_name]
            team_a_poss = float(data[i][2]) + 0.475 * float(data[i][3]) - float(data[i][4]) + float(data[i][5])
            team_b_poss = float(data[i + 1][2]) + 0.475 * float(data[i + 1][3]) - float(data[i + 1][4]) + float(data[i + 1][5])
            team_a_poss *= 0.96
            team_b_poss *= 0.96
            team_a.addGame(float(data[i][1]), float(team_a_poss), team_b_name, float(data[i + 1][1]),
                           float(team_b_poss), data[i][6][: len(data[i][6]) - 1])
            team_b.addGame(float(data[i + 1][1]), float(team_b_poss), team_a_name, float(data[i][1]),
                           float(team_a_poss), data[i + 1][6][: len(data[i + 1][6]) - 1])
            print('loadTeamsfromboxscores: ' + data[i][6][: len(data[i][6]) - 1])
    SportsRefScraper.update_defensive_ratings(teams)
    SportsRefScraper.update_adjusted_offensive_ratings(teams)
    return teams

def loadGameFile():
    teams = {}
    with open(Settings.DATA_FOLDER + 'gamefilerevised.csv', 'r') as gamefile:
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

    SportsRefScraper.update_defensive_ratings(teams)
    SportsRefScraper.update_adjusted_offensive_ratings(teams)
    return teams

def loadSchedule(teams):
    with open('teamSchedule.csv', 'r') as schedulefile:
        reader = csv.reader(schedulefile)
        lines = schedulefile.readlines()
        data = []
        for line in lines:
            data.append(line.split(','))
        teamHeader = True
        for row in data:
            if len(row[0]) > 1:
                if teamHeader:
                    team = teams[row[0][: len(row[0]) - 1]]
                    teamHeader = False
                elif str(row[0]) != 'Opponent':
                    print('loadschedule' + str(row))
                    team.addToSchedule(row[0], row[1], row[2])
            else:
                teamHeader = True
    return teams