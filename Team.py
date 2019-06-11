class Team:
    def __init__(self, teamName):
        self.oppTotalDefense = 0
        self.possessions = 0
        self.points = 0
        self.name = teamName
        self.defRating = 0
        self.games = 0
        self.gamedata = []
        self.adjPPP = 0
        self.schedule = []
        self.oppPoss = 0
        self.oppPoints = 0
        self.adjDef = 0

    def addGame(self, points, poss, oppName, oppPoints, oppPoss, id):
        self.possessions += float(poss)
        self.points += float(points)
        self.games += 1
        #self.oppPoss += oppPoss
        self.oppPoints += oppPoints
        self.gamedata.append({'points_per_pos_scored': float(points / poss), 'opponent_name': oppName,
                              'opponent_points': float(oppPoints),'opponent_poss': oppPoss, 'points' : points,
                              'possessions' : poss, 'game-id' : id})
        new_schedule = []
        for game in self.schedule:
            if game.get('game-id') != id:
                new_schedule.append(game)
        self.schedule.clear()
        self.schedule.extend(new_schedule)

    def PointsPerPos(self):
        if self.possessions > 0:
            return float(self.points) / float(self.possessions)
        return 0

    def addToSchedule(self, oppName, gameSite, gameId):
        addGame = True
        for game in self.schedule:
            if game.get('game-id') == gameId:
                addGame = False
        if addGame:
            self.schedule.append({'opponent-name' : oppName, 'game-id' : gameId, 'game-site': gameSite})

    def updateDefRating(self, pointsHeldTo, oppPoints, oppPoss):
        self.defRating += (float(oppPoints) - float(pointsHeldTo))
        self.oppPoss += oppPoss

    def defensiveRating(self):
        if self.games > 0:
            return (float(self.defRating)) / self.games
        else:
            return 0

    def updateOffensiveRating(self, points_per_pos, oppDef, poss):
        self.adjPPP += (float(points_per_pos) + float(oppDef))

    def updateAdjDefensiveRating(self, pppHeldTo, avgPPP):
        self.adjDef += (float(avgPPP) - float(pppHeldTo))

    def adjDefRating(self):
        if self.games > 0:
            return float(self.adjDef) / self.games
        else:
            return 0

    def OffensiveRating(self):
        if self.games > 0:
            return float(self.adjPPP) / self.games
        else:
            return 0

    def overallRating(self):
        return float(self.adjDefRating()) + float(self.OffensiveRating())

    def resetAdjOffensiveRating(self):
        self.adjPPP = 0

    def resetDefensiveRating(self):
        self.oppPoss = 0
        self.defRating = 0

    def resetAdjDefensiveRating(self):
        self.adjDef = 0