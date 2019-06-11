""" If True, creates a new power index database in the same folder as the program, or in the folder 'DATA_FOLDER' if
the length of that string > 0. If false, finds the database in DATA_FOLDER and updates. In both cases, the program finds
and uses data between the dates START_MONTH/START_DAY/START_YEAR and END_MONTH/END_DAY/END_YEAR, inclusive."""
CREATE_MODE = False
DATA_FOLDER = ''
START_MONTH = 12
START_DAY = 15
START_YEAR = 2018
UPDATE_MONTH = 3
UPDATE_DAY = 4
UPDATE_YEAR = 2019
END_MONTH = 3
END_DAY = 16
END_YEAR = 2018

"""GAME_PAGE_DELAY is the length of time, in seconds, between each call to BeautifulSoup to retrieve the page for a 
specific game.
GAME_INDEX_DELAY is the length of time between each call to get the page data for the index of games occurring on a 
particular date.
URLERROR_DELAY is the time the program waits when the site rejects a request from BeautifulSoup, throwing a URLERROR. 
This allows the program to continue running when it gets flagged for excessive data scraping, which is inevitable for
long date ranges."""
GAME_PAGE_DELAY = 4
GAME_INDEX_DELAY = 4
URLERROR_DELAY = 45

HOME_COURT_ADVANTAGE = 2 / 80.0

def getMonthLength(month, year):
    case = {
        1 : 31,
        2 : 28,
        3 : 31,
        4 : 30,
        5 : 31,
        6 : 30,
        7 : 31,
        8 : 31,
        9 : 30,
        10 : 31,
        11 : 30,
        12 : 31
    }
    return case.get(month, 0)