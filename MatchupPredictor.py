import csv
import TeamLoader
import SportsRefScraper
teams = TeamLoader.loadGameFile()
SportsRefScraper.updateDefensiveRatings(teams)
SportsRefScraper.updateAdjustedOffensiveRatings(teams)
predict_page = SportsRefScraper.getGameIndexPage(1, 12, 2019)
game_links = predict_page.find_all('a')
game_links = game_links[37:len(game_links) - 125]
print(game_links)

matchups = []
for i in range(0, len(game_links), 3):
    if str(game_links[i]).find('href=') > 0 and str(game_links[i + 2]).find('href=') > 0:
        matchups.append(SportsRefScraper.extractTeamName(str(game_links[i])))
        matchups.append(SportsRefScraper.extractTeamName(str(game_links[i + 2])))

with open('predictions.csv', 'a+') as predictionfile:
    predictionfile.write('1/12/2019' + '\n')
    for i in range(0, len(matchups), 2):
        print(matchups)
        team_a = teams[matchups[i]]
        team_b = teams[matchups[i + 1]]
        print(team_a.overallRating())
        print(team_b.overallRating())
        if float(team_a.overallRating()) > float(team_b.overallRating()):
            predictionfile.write(matchups[i] + ',' + matchups[i + 1] + '\n')
        else:
            predictionfile.write(matchups[i + 1] + ',' + matchups[i] + '\n')
