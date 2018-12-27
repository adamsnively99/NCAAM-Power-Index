import Settings
import SportsRefScraper
import Team
import DatabaseUpdater
if Settings.CREATE_MODE:
    teams = SportsRefScraper.createDatabase()
else:
    teams = DatabaseUpdater.loadGameFile()
    updatePage = SportsRefScraper.getGameIndexPage(Settings.START_MONTH, Settings.START_DAY, Settings.START_YEAR)
    SportsRefScraper.scrapeIndexPage(updatePage, teams)


Team.updateDefensiveRatings(teams)
Team.updateAdjustedOffensiveRatings(teams)
Team.writeTeamData(teams)
Team.writeGameData(teams)