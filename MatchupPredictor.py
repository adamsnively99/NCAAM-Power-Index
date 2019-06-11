import SportsRefScraper
from scipy.stats import norm

import Settings
import SportsRefScraper


def getGamesToPredict(month, day, year):
    predict_page = SportsRefScraper.getGameIndexPage(month, day, year)
    game_links = predict_page.find_all('a')
    game_links = game_links[37:len(game_links) - 125]
    matchups = []
    for i in range(0, len(game_links), 3):
        print(game_links[i])
        print(game_links[i + 1])
        if str(game_links[i]).find('href=') > 0 and str(game_links[i + 2]).find('href=') > 0:
            matchups.append(SportsRefScraper.extractTeamName(str(game_links[i])))
            matchups.append(SportsRefScraper.extractTeamName(str(game_links[i + 2])))
    return matchups

def getHomeCourtAdvantage(team_a, team_b):
    site = 0
    for game in team_a.schedule:
        if game.get('opponent-name') == team_b.name:
            return float(game.get('game-site')) * Settings.HOME_COURT_ADVANTAGE
    return 0

def predictGames(teams, fileName):
    matchups = getGamesToPredict(Settings.UPDATE_MONTH, Settings.UPDATE_DAY, Settings.UPDATE_YEAR)
    outcomes = getGameOutcomes()
    correct = 0
    incorrect = 0
    inconclusive = 0
    with open(fileName, 'a+') as predictionfile:
        predictionfile.write(str(Settings.UPDATE_MONTH) + '/' + str(Settings.UPDATE_DAY) + '\n')
        for i in range(0, len(matchups), 2):
            team_a = teams[matchups[i]]
            team_b = teams[matchups[i + 1]]
            home_court_advantage = getHomeCourtAdvantage(team_a, team_b)
            print('team a : ' + str(team_a.name))
            print('team b : ' + str(team_b.name))
            print('home court advantage : ' + str(home_court_advantage))
            z = ((team_a.overallRating() - team_b.overallRating() + home_court_advantage) - 0.1309763972321633) \
                / 0.1001385937018011
            odds = norm.cdf(z)
            predictionfile.write(matchups[i] + ',' + matchups[i + 1] + ',' + str(odds) + '\n')
            if float(team_a.overallRating()) + home_court_advantage > float(team_b.overallRating()):
                """if team_a.name == str(outcomes[int(i / 2)][:len(outcomes[int(i / 2)]) - 1]):
                    correct += 1
                elif team_b.name == str(outcomes[int(i / 2)][: len(outcomes[int(i / 2)]) - 1]):
                    incorrect +=1
                else:
                    print(team_a.name)
                    inconclusive += 1"""
            else:
                """if team_b.name == str(outcomes[int(i / 2)][: len(outcomes[int(i / 2)]) - 1]):
                    correct += 1
                elif team_a.name == str(outcomes[int(i / 2)][: len(outcomes[int(i / 2)]) - 1]):
                    incorrect +=1
                else:
                    print(team_b.name)
                    inconclusive += 1
        print(str(correct) + ' ' + str(incorrect) + ' ' + str(inconclusive))"""

def getGameOutcomes():
    outcomes = open('results113.txt')
    outcomelist = outcomes.readlines()
    print(outcomelist)
    return outcomelist