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

  def calculateScore(self,value,graphType):
    if self.accountFor:
      score = -1
      if value > self.ideal:
        if self.ub != -1:
          if value > self.ub:
            score = self.weight["ub"]["great"]["linear"] * (-1 * self.ub / value) + self.defaultScore["ub"]["great"]["linear"]
          else:
            score = self.weight["ub"]["less"]["linear"] * ( -1 * value / self.ub ) + self.defaultScore["ub"]["less"]["linear"]
        else:
          score = self.weight["ub"]["less"]["linear"]
      elif value < self.ideal:
        if value > self.lb:
          score = self.weight["lb"]["great"]["linear"] * (value / self.ideal) + self.defaultScore["lb"]["great"]["linear"]
        else:
          score = self.weight["lb"]["less"]["linear"] * (value / self.ideal) + self.defaultScore["lb"]["less"]["linear"]
      else:
        # you get a unicorn :)
        score = self.weight["lb"]["less"]["linear"]
    else:
      score = 0
    self.score = score
    return score

  def __str__(self):
    if self.lb == -1:
      return self.name  + " = " + " N/A DRV" + " ( " + str(self.value) + " " + self.unit + " / " + str(self.score) + ") "
    else:
      return self.name  + " = " + "{0:.1f}".format(float(float(self.value) / float(self.ideal)) * 100) + "% of Ideal" + " ( " + str(self.value) + " " + self.unit + " / " + str(self.score) + ") "

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
    self.fails = 0
    self.met = False