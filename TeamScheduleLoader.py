import time
from bs4 import BeautifulSoup
import urllib
import Settings
import TeamLoader
import SportsRefScraper

def getTeamSchedule(teamName):
    URLRetrieval = False
    while not URLRetrieval:
        try:
            with urllib.request.urlopen('https://www.sports-reference.com/cbb/schools/' + teamName + '/2019-schedule.html') as response:
                page = response.read()
                pageSoup = BeautifulSoup(page, 'html.parser')
                schedule = pageSoup.select('#div_schedule')
                URLRetrieval = True
        except urllib.error.URLError:
            print('URL Request Failed')
            time.sleep(Settings.URLERROR_DELAY)
    return schedule

def writeSchedules(teams):
    with open('teamSchedule.csv', 'w') as out:
        gameid = 0
        for teamName in teams:
            out.write('\n' + teamName + '\n' + 'Opponent' + ',' + 'Location' + ',' + 'gameid' + '\n')
            print(teamName)
            schedule = getTeamSchedule(teamName)[0]
            alllocations = schedule.find_all(attrs={'data-stat' : 'game_location'})[1:]
            tableLinks = schedule.find_all(attrs={'data-stat' : 'opp_name'})[1:]
            opponents = []
            locations = []
            for i in range(len(tableLinks)):
                if str(tableLinks[i]).find('cbb/schools') > -1 and str(tableLinks[i]).find('cbb/boxscores/') < 0:
                    opponents.append(tableLinks[i])
                    locations.append(alllocations[i])
            for i in range(len(opponents)):
                gameid += 1
                location = locations[i]
                location = str(location)[str(location).find('>') + 1]
                gameSite = 1
                if location is '@':
                    gameSite = -1
                elif location is 'N':
                    gameSite = 0
                opponent = str(opponents[i]).find('/cbb/schools/')
                endOpponent = str(opponents[i]).find('/2019.html')
                opponentName = str(opponents[i])[opponent  + 13: endOpponent]
                print(opponentName + ' ' + str(gameSite))
                out.write(opponentName + ',' + str(gameSite) + ',' + str(gameid) + '\n')
            time.sleep(3)


teams = TeamLoader.loadGameFile()
SportsRefScraper.updateDefensiveRatings(teams)
SportsRefScraper.updateAdjustedOffensiveRatings(teams)
writeSchedules(teams)