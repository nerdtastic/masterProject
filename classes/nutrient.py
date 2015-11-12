class Nutrient():
  def getName(self):
    return self.name

  def getUnit(self):
    return self.unit

  def getLowerBound(self):
    return self.lb

  def getUpperBound(self):
    return self.ub

  def getId(self):
    return self.id

  def getValue(self):
    return self.value
  def getScore(self):
    return self.score
  def calculateScore(self, graphType):

    if self.accountFor:
      score = -1
      if self.value > self.ideal:
        if self.ub != -1:
          if self.value > self.ub:
            score = self.weight["ub"]["great"]["linear"] * min(abs(self.ub / self.value), 1) + self.defaultScore["ub"]["great"]["linear"]
          else:
            score = self.weight["ub"]["less"]["linear"] * ( -1 * self.value / self.ub ) + self.defaultScore["ub"]["less"]["linear"]
        else:
          score = 1
      elif self.value < self.ideal:
        if self.value > self.lb:
          score = self.weight["lb"]["great"]["linear"] * (self.value / self.ideal) + self.defaultScore["lb"]["great"]["linear"]
        else:
          score = self.weight["lb"]["less"]["linear"] * (self.value / self.ideal) + self.defaultScore["lb"]["less"]["linear"]
        # 
      else:
        #you get a unicorn :)
        score = 1
    else:
      score = 0
    self.score = score
    return score

  def __str__(self):
    if self.lb == -1:
      return self.name  + " = " + " N/A DRV" + " ( " + str(self.value) + " " + self.unit + " / " + str(self.score) + ") "
    else:
      return self.name  + " = " + "{0:.1f}".format(float(float(self.value) / float(self.ideal)) * 100) + "% DRV" + " ( " + str(self.value) + " " + self.unit + " / " + str(self.score) + ") "

  def __init__(self, name, unit, lb, ub, ideal, id, value, accountFor, weight, defaultScore):
    self.name = name
    self.unit = unit
    self.lb = lb
    self.ideal = ideal
    self.ub = ub
    self.id = id
    self.value = value
    self.accountFor = accountFor
    self.weight = weight
    self.defaultScore = defaultScore
    self.score = -1 if self.accountFor else 0