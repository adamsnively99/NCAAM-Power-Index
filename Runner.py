import Settings
import SportsRefScraper
import Team
import DatabaseUpdater
if Settings.CREATE_MODE:
    teams = SportsRefScraper.createDatabase()
else:
    teams = DatabaseUpdater.loadGameFile()
    updatePage = SportsRefScraper.getGameIndexPage(Settings.START_MONTH, Settings.START_DAY, Settings.START_YEAR)
    teams = SportsRefScraper.scrapeIndexPage(updatePage, teams)


SportsRefScraper.updateDefensiveRatings(teams)
SportsRefScraper.updateAdjustedOffensiveRatings(teams)
SportsRefScraper.writeTeamData(teams)
SportsRefScraper.writeGameData(teams)