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

    def addGame(self, points, poss, oppName, oppPointsPerPos):
        self.possessions += float(poss)
        self.points += float(points)
        self.games += 1
        self.gamedata.append({'points_per_pos_scored': float(points / poss), 'opponent_name': oppName,
                              'opponent_points_per_pos': float(oppPointsPerPos), 'points' : points, 'possessions' : poss})

    def PointsPerPos(self):
        return float(self.points) / float(self.possessions)

    def updateDefRating(self, pointsHeldTo, oppPointsPerPos):
        self.defRating += (float(oppPointsPerPos) - float(pointsHeldTo))

    def defensiveRating(self):
        return float(self.defRating) / float(self.games)

    def updateOffensiveRating(self, points_per_pos, oppDef):
        self.adjPPP += float(points_per_pos) + float(oppDef)

    def OffensiveRating(self):
        return float(self.adjPPP) / float(self.games)