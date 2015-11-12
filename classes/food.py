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

  def __str__(self):
    return self.name + " - " + self.group

  def __init__(self, id, name, unit, amount, group):
    self.id = id
    self.name = name
    self.unit = unit
    self.amount = amount
    self.group = group
