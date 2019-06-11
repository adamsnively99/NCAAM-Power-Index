import TeamLoader
from Team import Team
import SportsRefScraper
from scipy.stats import norm
import numpy
import matplotlib
import MatchupPredictor

def load_game_from_box_score(data, teams, i):
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
    team_b_poss *= 0.96
    team_a_poss *= 0.96
    team_a.addGame(float(data[i][1]), float(team_a_poss), team_b_name, float(data[i + 1][1]),
                   float(team_b_poss), data[i][6][: len(data[i][6]) - 1])
    team_b.addGame(float(data[i + 1][1]), float(team_b_poss), team_a_name, float(data[i][1]),
                   float(team_a_poss), data[i + 1][6][: len(data[i + 1][6]) - 1])
   # print('loadTeamsfromboxscores: ' + data[i][6][: len(data[i][6]) - 1])


def load_teams_from_schedule():
    with open('teamSchedule.csv', 'r') as schedulefile:
        lines = schedulefile.readlines()
        data = []
        teams = {}
        for line in lines:
            data.append(line.split(','))
        teamHeader = True
        for row in data:
            if len(row[0]) > 1:
                if teamHeader:
                    team_name = row[0][: len(row[0]) - 1]
                    team = Team(team_name)
                    teams[team_name] = team
                    teamHeader = False
                elif str(row[0]) != 'Opponent':
                    print('loadschedule' + str(row))
                    team.addToSchedule(row[0], row[1], row[2])
            else:
                teamHeader = True
        return teams

def get_ratings(teams):
    teamRatings = []
    for team in teams:
        teamRatings.append(teams[team].overallRating())
    return teamRatings

def find_rating_mean(teams):
    teamRatings = get_ratings(teams)
    teamRatings.sort()
    difference = []
    for i in range(len(teamRatings)):
        for j in range(i + 1, len(teamRatings)):
            difference.append(teamRatings[j] - teamRatings[i])
    return numpy.mean(difference)

def find_rating_stdev(teams):
    team_ratings = get_ratings(teams)
    """team_ratings.sort()
    difference = []
    for i in range(len(team_ratings)):
        for j in range(i + 1, len(team_ratings)):
            difference.append(team_ratings[j] - team_ratings[i])"""
    return numpy.std(team_ratings)

def find_bucket(buckets, val):
    i = 0
    while val > buckets[i]:
        i += 1
    return i

buckets = [.10, .20, .30, .40, .50, .60, .70, .80, .90, 1]
wins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
games = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hits = 0
total_games = 0
teams = load_teams_from_schedule()
with open('boxscoredata.csv', 'r') as file:
    lines = file.readlines()
    data = []
    for line in lines:
        data.append(line.split(','))
    for i in range(0, len(data), 2):
        load_game_from_box_score(data, teams, i)
        if i > 1000:
            SportsRefScraper.update_defensive_ratings(teams)
            SportsRefScraper.update_adjusted_offensive_ratings(teams)
            SportsRefScraper.update_adjusted_defensive_ratings(teams)
            team_a = teams[data[i][0]]
            team_b = teams[data[i + 1][0]]
            home_court_advantage = MatchupPredictor.getHomeCourtAdvantage(team_a, team_b)
            z = (team_a.overallRating() - team_b.overallRating() - home_court_advantage) \
                / find_rating_stdev(teams)
            odds = norm.cdf(z)


            total_games += 1
            bucket_index = find_bucket(buckets, odds)
            games[bucket_index] += 1
            if float(data[i][1]) > float(data[i + 1][1]):
                if odds > 0.50:
                    hits += 1
                wins[bucket_index] += 1
            elif odds < 0.5:
                hits += 1
            print(data[i][0] + ' has a ' + str(odds) + 'chance of beating ' + data[i + 1][0])

for i in range(len(buckets)):
    print(str(buckets[i] - 0.1) + '-' + str(buckets[i]) + ': ' + str(wins[i]) + '/' + str(games[i]) + ' = ' +
          str(float(wins[i]) / games[i]))

print('Total accuracy: ' + str(float(hits / total_games)))