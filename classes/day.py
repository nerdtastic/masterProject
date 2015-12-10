class Day():
  def met(self):
    met = True
    for nutrient in self.nutrients:
      if not self.nutrients[nutrient].met and self.nutrients[nutrient].accountFor:
        met = False
        break
    return met

  def getDate(self):
    return self.date
  #this method will remove the food with the largest amount of nutrientId

  def refresh (self, removeFails):
    #zero out all nutrients
    for nutrient in self.nutrients:
      self.nutrients[nutrient].value = 0
      if removeFails:
        self.nutrients[nutrient].fails = 0

    #loop all foods
    for foodId, food in self.foods.iteritems():
      for nutrient in food.nutrients:
        if nutrient["nutrient_id"] in self.nutrients:
          self.nutrients[nutrient["nutrient_id"]].value += nutrient["value"]

    #calculate score
    self.score = 0
    for nutrient in self.nutrients:
      self.nutrients[nutrient].met = self.nutrients[nutrient].value > self.nutrients[nutrient].lb
      self.score += self.nutrients[nutrient].calculateScore(self.nutrients[nutrient].value,'linear')

  def replaceFood (self, nutrientId):
    nutMax = 0
    foodToRemove = -1
    for foodId, food in self.foods.iteritems():
      nutrientInFood = food.getNutrients()
      for nutrient in nutrientInFood:
        if nutrientId == nutrient["nutrient_id"] and nutrient["value"] > nutMax:
            nutmax = float(nutrient["value"])
            foodToRemove = foodId
            break
    del self.foods[foodToRemove]
    self.refresh(True)

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

    return "This report is for date: " + str(self.date) + str(self.met()) +". The score is: " + str(self.score) + "\n" + nutrientString + "\n" + foodString + "\n" #+ snapShotString

  def __init__(self, date, nutrients, foods, score, snapshots):
    self.date = date
    self.nutrients = nutrients
    self.foods = foods
    self.score = score
    self.snapshots = []