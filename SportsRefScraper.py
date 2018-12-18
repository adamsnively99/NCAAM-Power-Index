import csv
import requests
import time
import random
from bs4 import BeautifulSoup
import urllib
from Team import Team

# TODO: Allow user to differentiate between creating a database and updating an existing one
# TODO: Iterate over mined data to calculate each teams' defensive rating
# TODO: Iterate over mined data and use defensive ratings to calculate each teams adjusted points per possesion
# TODO: Remove dead code (a LOT was found to be unnecessary as I got to understand BeautifulSoup more)

def extractGameLink(item):
    startIndex = item.find('"')
    return 'https://www.sports-reference.com' + str(item[startIndex + 1:len(item) - 11])

def extractTeamName(item):
    print('ExtractTeamName:' + str(item))
    startIndex = item.find('schools/')
    endIndex = item.find('/2019')
    name = item[startIndex + 8: endIndex]
    print(name)
    return name.lower()

def extractTableHeaders(headerList):
    team_one = str(headerList[4])
    team_two = str(headerList[6])
    team_one = extractTeamName(team_one[:len(team_one) - 10])
    team_two = extractTeamName(team_two[:len(team_two) - 10])
    return team_one.lower(), team_two.lower()

def calcPossessionsFromTable(table, team):
    fieldGoalAttempts = float(table.find(attrs={'data-stat': 'fga'}).string)
    freeThrowAttempts = float(table.find(attrs={'data-stat': 'fta'}).string)
    offensiveRebounds = float(table.find(attrs={'data-stat': 'orb'}).string)
    turnovers = float(table.find(attrs={'data-stat': 'tov'}).string)
    return float((fieldGoalAttempts + 0.475 * freeThrowAttempts - offensiveRebounds + turnovers))

def getDivisionOneGames(totalGames):
    games = []
    for i in range(0, len(totalGames), 3):
        if str(totalGames[i]).find('href=') > 0 and str(totalGames[i + 2]).find('href=') > 0:
            games.append(extractTeamName(str(totalGames[i])))
            games.append(extractGameLink(str(totalGames[i + 1])))
            games.append(extractTeamName(str(totalGames[i + 2])))
    return games

def getGameIndexPage(month, day, year):
    gameUrl = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month=' + str(month) + '&day=' + str(day) + '&year=' + str(year)
    with urllib.request.urlopen(gameUrl) as siteResponse:
        gamePage = siteResponse.read()
    page = BeautifulSoup(gamePage, 'html.parser')
    return page



for i in range(0, 23, 1):
    pageSoup = getGameIndexPage(11, 6 + i, 2018)
    totalGames = pageSoup.find_all('a')
    totalGames = totalGames[37:len(totalGames) - 124]
    teams = {}
    gamesToScrape = getDivisionOneGames(totalGames)

    for j in range(1, len(gamesToScrape), 3):
        with urllib.request.urlopen(gamesToScrape[j]) as siteResponse:
            singleGamePage = siteResponse.read()
        gameSoup = BeautifulSoup(singleGamePage, 'html.parser')

        # Find names of teams
        team_table_headers = gameSoup.find_all('h2')
        team_a = gamesToScrape[j - 1]
        team_b = gamesToScrape[j + 1]

        # Instantiate Teams, if not already instantiated
        if team_a not in teams:
            teams[team_a] = Team(team_a)
        if team_b not in teams:
            teams[team_b] = Team(team_b)

        # Find box score data for each team from game
        team_a_table = gameSoup.select('#div_box-score-basic-' + team_a)
        team_b_table = gameSoup.select('#div_box-score-basic-' + team_b)
        team_a_stats = team_a_table[0].find('tfoot')
        team_b_stats = team_b_table[0].find('tfoot')

        teams[team_a].addGame(float(team_a_stats.find(attrs={'data-stat': 'pts'}).string),
                               calcPossessionsFromTable(team_a_stats, team_a), team_b,
                          float(team_b_stats.find(attrs={'data-stat': 'pts'}).string) / calcPossessionsFromTable(team_b_stats, team_b))
        time.sleep(random.uniform(5, 10))

with open ('BPI2018-19', 'w') as outfile:
    for team in teams:
        outfile.write(str(teams[team].name) + ',')
        outfile.write(str(teams[team].PointsPerPos()) + ',' + '\n')

with open ('gamefile', 'w') as outfile:
    for team in teams:
        outfile.write(team + ',\n Opponent, PointsPerPos Scored, PointsPerPos Allowed, \n')
        for game in teams[team].gamedata:
            outfile.write(str(game['opponent_name']) + ',' + str(game['points_per_pos_scored']) + ',' +
                          str(game['opponent_points_per_pos']) + '\n')
        outfile.write('\n')

