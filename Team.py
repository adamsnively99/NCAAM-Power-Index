class Team:
    def __init__(self, teamName):
        self.oppTotalDefense = 0
        self.possessions = 0
        self.points = 0
        self.name = teamName
        self.defRating = 0
        self.games = 0
        self.gamedata = []

    def addGame(self, points, poss, oppName, oppPointsPerPos):
        self.possessions += poss
        self.points += points
        self.games += 1
        self.gamedata.append({'points_per_pos_scored': float(points / poss), 'opponent_name': oppName,
                              'opponent_points_per_pos': oppPointsPerPos})

    def PointsPerPos(self):
        return self.points / self.possessions
    
    def updateDefRating(self, pointsHeldTo, oppPointsPerPos):
        self.defRating += (float(oppPointsPerPos) - float(pointsHeldTo))

    def defensiveRating(self):
        return self.defRating / self.games