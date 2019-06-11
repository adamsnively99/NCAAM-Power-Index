import time
from bs4 import BeautifulSoup
import urllib
import requests
from Team import Team
import Settings
# TODO: Organize and document, like, all of this

def extract_game_link(item):
    startIndex = item.find('"')
    return 'https://www.sports-reference.com' + str(item[startIndex + 1:len(item) - 11])

def extract_team_name(item):
    startIndex = item.find('schools/')
    endIndex = item.find('/2019')
    name = item[startIndex + 8: endIndex]
    return name.lower()

def extract_table_headers(headerList):
    team_one = str(headerList[4])
    team_two = str(headerList[6])
    team_one = extract_team_name(team_one[:len(team_one) - 10])
    team_two = extract_team_name(team_two[:len(team_two) - 10])
    return team_one.lower(), team_two.lower()

def calc_possessions_from_table(table, team):
    fieldGoalAttempts = float(table.find(attrs={'data-stat': 'fga'}).string)
    freeThrowAttempts = float(table.find(attrs={'data-stat': 'fta'}).string)
    offensiveRebounds = float(table.find(attrs={'data-stat': 'orb'}).string)
    turnovers = float(table.find(attrs={'data-stat': 'tov'}).string)
    return float((fieldGoalAttempts + 0.475 * freeThrowAttempts - offensiveRebounds + turnovers))

"""Returns list of strings where the length is divisible by three, every three entries forms a tuple where entries zero 
and two are team names, and entry one is the link to the game page"""
def get_division_one_games(totalGames):
    games = []
    print('getd1gamestotal' + str(totalGames))
    print(len(totalGames))
    for i in range(0, len(totalGames), 3):

        print('get d1 games loop' + str(totalGames[i]))
        if str(totalGames[i]).find('href=') > 0 and str(totalGames[i + 2]).find('href=') > 0:
            games.append(extract_team_name(str(totalGames[i])))
            games.append(extract_game_link(str(totalGames[i + 1])))
            games.append(extract_team_name(str(totalGames[i + 2])))
    print(games)
    return games

#Gets BeautifulSoup html parsing of game page
def get_game_index_page(month, day, year):
    gameUrl = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month=' + str(month) + '&day=' + str(day) + \
              '&year=' + str(year)
    return get_page_soup(gameUrl)

def write_team_data(teams):
    with open('BPI2018-19.csv', 'w') as outfile:
        for team in teams:
            outfile.write(str(teams[team].name) + ',')
            outfile.write(str(teams[team].games) + ',')
            outfile.write(str(teams[team].points) + ',')
            outfile.write(str(teams[team].possessions) + ',')
            outfile.write(str(teams[team].OffensiveRating()) + ',')
            outfile.write(str(teams[team].defensiveRating()) + ',' + '\n')

def write_game_data(teams):
    with open('gamefile.csv', 'w') as outfile:
        for team in teams:
            outfile.write(team + ',\n Opponent, PointsPerPos Scored, OppPos Allowed, Opp Pos \n')
            for game in teams[team].gamedata:
                outfile.write(str(game['opponent_name']) + ',' + str(game['points_per_pos_scored']) + ',' +
                              str(game['opponent_points']) + ',' + str(game['opponent_poss']) +','+
                              str(game['points']) + ',' + str(game['possessions']) +'\n')
            outfile.write('\n')


def get_box_score_data(soup, team_name):
    team_table = soup.select('#div_box-score-basic-' + team_name)
    return team_table[0].find('tfoot')

def update_adjusted_offensive_ratings(team_dict):
    for team in team_dict:
        current_team = team_dict[team]
        current_team.resetAdjOffensiveRating()
        for game in current_team.gamedata:
            current_team.updateOffensiveRating(game['points_per_pos_scored'],
                                               team_dict[game['opponent_name']].defensiveRating(), game['possessions'])

def update_adjusted_defensive_ratings(teams):
    for team in teams:
        current_team = teams[team]
        current_team.resetAdjDefensiveRating()
        for game in current_team.gamedata:
            current_team.updateAdjDefensiveRating(game['opponent_points'] / game['opponent_poss'],
                                                  teams[game['opponent_name']].OffensiveRating())

def update_defensive_ratings(team_dict):
    for team in team_dict:
        current_team = team_dict[team]
        current_team.resetDefensiveRating()
        for game in current_team.gamedata:
            try:
                current_team.updateDefRating(game['opponent_points'] / game['opponent_poss'], team_dict[game['opponent_name']].PointsPerPos(), game['opponent_poss'])
            except ZeroDivisionError:
                print(team + ' caused a zero division error')

def get_page_soup(link):
    urlRetrieved = False
    while not urlRetrieved:
        try:
            with urllib.request.urlopen(link) as siteResponse:
                singleGamePage = siteResponse.read()
            gameSoup = BeautifulSoup(singleGamePage, 'html.parser')
            urlRetrieved = True
            time.sleep(Settings.GAME_INDEX_DELAY)
            print('Sleep')
        except urllib.error.URLError:
            print('URL Request failed')
            time.sleep(Settings.URLERROR_DELAY)
    return link

#Uses game links on index page to update teams
def scrape_index_page(page, teams):
    totalGames = page.find_all('a')
    totalGames = totalGames[37:len(totalGames) - 125]
    gamesToScrape = get_division_one_games(totalGames)
    for j in range(1, len(gamesToScrape), 3):
        gameSoup = get_page_soup(gamesToScrape[j])
        # Find names of teams
        team_a = gamesToScrape[j - 1]
        team_b = gamesToScrape[j + 1]

        # Instantiate Teams, if not already instantiated
        if team_a not in teams:
            teams[team_a] = Team(team_a)
        if team_b not in teams:
            teams[team_b] = Team(team_b)

        update_teams_from_game_data(gameSoup, teams, team_a, team_b)

    return teams

def update_teams_from_game_data(gameSoup, teams, team_a, team_b):
    # Find box score data for each team from game
    team_a_stats = get_box_score_data(gameSoup, team_a)
    team_b_stats = get_box_score_data(gameSoup, team_b)

    teams[team_a].addGame(float(team_a_stats.find(attrs={'data-stat': 'pts'}).string),
                          calc_possessions_from_table(team_a_stats, team_a), team_b,
                          float(
                              team_b_stats.find(attrs={'data-stat': 'pts'}).string) / calc_possessions_from_table(
                              team_b_stats, team_b))
    teams[team_b].addGame(float(team_b_stats.find(attrs={'data-stat': 'pts'}).string),
                          calc_possessions_from_table(team_b_stats, team_b), team_a,
                          float(
                              team_a_stats.find(attrs={'data-stat': 'pts'}).string) / calc_possessions_from_table(
                              team_a_stats, team_a))


def createDatabase():
    day = Settings.START_DAY
    month = Settings.START_MONTH
    year = Settings.START_YEAR
    teams = {}
    while day != Settings.END_DAY or month != Settings.END_MONTH or year != Settings.END_YEAR:
        pageSoup = get_game_index_page(month, day, year)
        scrape_index_page(pageSoup, teams)

        if day == Settings.getMonthLength(month, year):
            day = 1
            month +=1
            if month == 13:
                month = 1
                year += 1
        else:
            day += 1
    return teams

def write_game_stats(file, team_stats, team_name, gameid):
    file.write(team_name + ',' + team_stats.find(attrs={'data-stat': 'pts'}).string + ',' +
               team_stats.find(attrs={'data-stat': 'fga'}).string
                  + ',' + team_stats.find(attrs={'data-stat': 'fta'}).string + ',' +
               team_stats.find(attrs={'data-stat': 'orb'}).string
                  + ',' + team_stats.find(attrs={'data-stat': 'tov'}).string + ',' + str(gameid) + '\n')