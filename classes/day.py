class Day():
  def getDate(self):
    return self.date

  def getNutrients(self):
    return self.nutrients

  def getFoods(self):
    return self.foods

  def getScore(self):
    return self.score

  def __str__(self):
    nutrientString = "\033[4mNutrient List\033[0m\n"
    foodString = "\033[4mFood List\033[0m\n"
    snapShotString = "\033[4mSnapshot scores\033[0m\n"
    for nutrient in self.nutrients:
      nutrientString = nutrientString + str(self.nutrients[nutrient]) + "\n"
    for food in self.foods:
      foodString = foodString + str(self.foods[food]) + "\n"
    for snapshot in self.snapshots:
      snapShotString = snapShotString + str(snapshot) + "\n"

    return "This report is for date: " + str(self.date) + ". The score is: " + str(self.score) + "\n" + nutrientString + "\n" + foodString + "\n" + snapShotString

  def __init__(self, date, nutrients, foods, score, snapshots):
    self.date = date
    self.nutrients = nutrients
    self.foods = foods
    self.score = score
    self.snapshots = []