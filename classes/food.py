class Food():
  def getId(self):
    return self.id

  def getName(self):
    return self.name

  def getAmount(self):
    return self.amount

  def getUnit(self):
    return self.unit

  def getFoodGroup(self):
    return self.group

  def getNutrients(self):
    return self.nutrients

  def __str__(self):
    return self.name + " - " + self.group

  def __init__(self, id, name, group, nutrients):
    self.id = id
    self.name = name
    self.group = group
    self.nutrients = nutrients