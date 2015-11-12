class Snapshot():
  def getDate(self):
    return self.date

  def getNutrients(self):
    return self.nutrients

  def getFoods(self):
    return self.foods

  def getScore(self):
    return self.score

  def __str__(self):
    return str(self.score)

  def __init__(self, nutrients, foods, score):
    self.nutrients = nutrients
    self.foods = foods
    self.score = score