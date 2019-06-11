from matplotlib import pyplot

import Settings
import SportsRefScraper
import MatchupPredictor
import TeamLoader
import matplotlib
import numpy

if Settings.CREATE_MODE:
    teams = SportsRefScraper.createDatabase()
else:
    teams = TeamLoader.loadTeamsFromBoxScores()
    #teams = TeamLoader.loadSchedule(teams)
    #MatchupPredictor.predictGames(teams, 'predictions_revised.csv')
    #updatePage = SportsRefScraper.getGameIndexPage(Settings.UPDATE_MONTH, Settings.UPDATE_DAY, Settings.UPDATE_YEAR)
    #teams = SportsRefScraper.scrapeIndexPage(updatePage, teams)
    #SportsRefScraper.updateDefensiveRatings(teams)
    #SportsRefScraper.updateAdjustedOffensiveRatings(teams)

    SportsRefScraper.write_team_data(teams)
    SportsRefScraper.write_game_data(teams)


"""
buckets = numpy.linspace(0.6, 1.41, num=25)
teamRatings = []
indices = numpy.linspace(1, 25, 25)
bucketCounts = []
bucketCounts.append(0)
#print(indices)
for team in teams:
    teamRatings.append(teams[team].overallRating())

teamRatings.sort()
bucket = 0
difference = []
for i in range(len(teamRatings)):
    rating = teamRatings[i]
    #print(str(rating) + ", " + str(buckets[i]))
    for j in range(i + 1, len(teamRatings)):
        difference.append(teamRatings[j] - teamRatings[i])
    if float(rating) > float(buckets[bucket]):
        bucket += 1
        bucketCounts.append(bucketCounts[bucket - 1])
    bucketCounts[bucket] += 1

matplotlib.pyplot.plot(buckets, bucketCounts)
matplotlib.pyplot.show()
print('avg rating: ' + str(numpy.mean(teamRatings)))
print('avg difference: ' + str(numpy.mean(difference)))
print('std ratings: ' + str(numpy.std(teamRatings)))
print('std difference: ' + str(numpy.std(difference)))"""