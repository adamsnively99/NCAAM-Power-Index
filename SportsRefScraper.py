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
    startIndex = item.find('schools/')
    endIndex = item.find('/2019')
    name = item[startIndex + 8: endIndex]
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

    print(games)
    return games

def getGameIndexPage(month, day, year):
    gameUrl = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month=' + str(month) + '&day=' + str(day) + '&year=' + str(year)
    urlRetrieved = False
    while not urlRetrieved:
        try:
            with urllib.request.urlopen(gameUrl) as siteResponse:
                gamePage = siteResponse.read()
            page = BeautifulSoup(gamePage, 'html.parser')
            urlRetrieved = True
        except urllib.error.URLError:
            time.sleep(300)
    return page

def writeTeamData(teams):
    with open('BPI2018-19.csv', 'w') as outfile:
        for team in teams:
            outfile.write(str(teams[team].name) + ',')
            outfile.write(str(teams[team].games) + ',')
            outfile.write(str(teams[team].points) + ',')
            outfile.write(str(teams[team].possessions) + ',')
            outfile.write(str(teams[team].OffensiveRating()) + ',')
            outfile.write(str(teams[team].defensiveRating()) + ',' + '\n')

def writeGameData(teams):
    with open('gamefile.csv', 'w') as outfile:
        for team in teams:
            outfile.write(team + ',\n Opponent, PointsPerPos Scored, PointsPerPos Allowed, \n')
            for game in teams[team].gamedata:
                outfile.write(str(game['opponent_name']) + ',' + str(game['points_per_pos_scored']) + ',' +
                              str(game['opponent_points_per_pos']) + '\n')
            outfile.write('\n')

def getBoxScoreData(soup, team_name):
    team_table = soup.select('#div_box-score-basic-' + team_name)
    return team_table[0].find('tfoot')

def createDatabase():
    days = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    month = 11
    teams = {}
    for i in days:
        if i == 1:
            month += 1

        pageSoup = getGameIndexPage(month, i, 2018)
        totalGames = pageSoup.find_all('a')
        totalGames = totalGames[37:len(totalGames) - 124]
        gamesToScrape = getDivisionOneGames(totalGames)
        for j in range(1, len(gamesToScrape), 3):
            urlRetrieved = False
            while not urlRetrieved:
                try:
                    with urllib.request.urlopen(gamesToScrape[j]) as siteResponse:
                        singleGamePage = siteResponse.read()
                    gameSoup = BeautifulSoup(singleGamePage, 'html.parser')
                    urlRetrieved = True
                except urllib.error.URLError:
                    time.sleep(300)
            # Find names of teams
            team_a = gamesToScrape[j - 1]
            team_b = gamesToScrape[j + 1]

            # Instantiate Teams, if not already instantiated
            if team_a not in teams:
                teams[team_a] = Team(team_a)
            if team_b not in teams:
                teams[team_b] = Team(team_b)

            # Find box score data for each team from game
            team_a_stats = getBoxScoreData(gameSoup, team_a)
            team_b_stats = getBoxScoreData(gameSoup, team_b)
            teams[team_a].addGame(float(team_a_stats.find(attrs={'data-stat': 'pts'}).string),
                                  calcPossessionsFromTable(team_a_stats, team_a), team_b,
                                  float(
                                      team_b_stats.find(attrs={'data-stat': 'pts'}).string) / calcPossessionsFromTable(
                                      team_b_stats, team_b))
            teams[team_b].addGame(float(team_b_stats.find(attrs={'data-stat': 'pts'}).string),
                                  calcPossessionsFromTable(team_b_stats, team_b), team_a,
                                  float(
                                      team_a_stats.find(attrs={'data-stat': 'pts'}).string) / calcPossessionsFromTable(
                                      team_a_stats, team_a))
            time.sleep(5)
        time.sleep(30)
    return teams



validInput = False
while not validInput:
    print('Would you like to create a new database or update an existing one? Type \'create\' or \'update\':')
    user_input = input()
    validInput = user_input == 'create' or user_input == 'update'

teams = {}
if user_input == 'create':
    teams = createDatabase()

for team in teams:
    current_team = teams[team]
    for game in current_team.gamedata:
        try:
            current_team.updateDefRating(game['opponent_points_per_pos'], teams[game['opponent_name']].PointsPerPos())
        except ZeroDivisionError:
            print(team + ' caused a zero division error')

for team in teams:
    current_team = teams[team]
    for game in current_team.gamedata:
        current_team.updateOffensiveRating(game['points_per_pos_scored'], teams[game['opponent_name']].defensiveRating())

writeTeamData(teams)
writeGameData(teams)