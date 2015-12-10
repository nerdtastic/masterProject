import random
import requests
import json
import time
import sys
import csv
from classes.snapshot import Snapshot
from classes.nutrient import Nutrient
from classes.day import Day
from classes.food import Food

api_key = "mgj10CavRUNan0tGpl316nAdfq2AwFptv5HVyLAc"

def main():
  today = Day(time.strftime("%x"), readFile( sys.argv[1] ), {},0, None)
  while not today.met():
    for name, nutrient in today.nutrients.iteritems():
      if nutrient.fails > 3:
        print "Removing a food for " + nutrient.name
        today.replaceFood(nutrient.id)
      elif not nutrient.met and nutrient.accountFor:
        print "Looking for " + nutrient.name
        food = getFoodForNutrient( nutrient)
        today.snapshots.append(calculateFood(food[random.randint(1, 100)]["ndbno"], today))
    print today
  print today

def calculateFood ( id , day):
  response = getResponse("http://api.nal.usda.gov/ndb/reports/?ndbno=" + str(id) + "&type=f&format=json&api_key=" + api_key)
  nutrients = response["report"]["food"]["nutrients"]
  foundFit = True
  newScore = 0

  for nutrient in nutrients:
    if nutrient["nutrient_id"] in day.nutrients:
      tempValue = day.nutrients[nutrient["nutrient_id"]].value + float(nutrient["value"])
      if day.nutrients[nutrient["nutrient_id"]].ub > 0 and tempValue > day.nutrients[nutrient["nutrient_id"]].ub:
        day.nutrients[nutrient["nutrient_id"]].fails += 1
        print "Exceeded " + day.nutrients[nutrient["nutrient_id"]].name + " (" + str(day.nutrients[nutrient["nutrient_id"]].fails) + ")."
        foundFit = False
        break
      else:
        newScore += day.nutrients[nutrient["nutrient_id"]].calculateScore(tempValue, "linear")
  #if the food fit add it to the day, and update all nutrients
  if foundFit:
    day.foods[id] = Food(id, response["report"]["food"]["name"], response["report"]["food"]["fg"], nutrients)
    day.refresh(False)
  tempSnapShot = Snapshot(day.nutrients,day.foods,day.score)
  return tempSnapShot

def getResponse ( url ):
  r = requests.get(url)
  response = json.loads(r.text)
  return response

def getFoodForNutrient( nutrient ):
  response = getResponse("http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key="+ api_key +"&nutrients="+ str(nutrient.id) +"&sort=c")
  foods = response["report"]["foods"]
  #before this call is where you could make it be random / select certain food group
  return foods

def readFile ( filename ):
  nutrientDict = {}
  NAME = 0
  UNIT = 1
  LB = 2
  UB = 3
  IDEAL = 4
  ID = 5
  ACCOUNTFOR = 6
  WEIGHTLTLB = 7
  WEIGHTGTLB = 8
  WEIGHTLTUB = 9
  WEIGHTGTUB = 10
  DEFAULTLTLB = 11
  DEFAULTGTLB = 12
  DEFAULTLTUB = 13
  DEFAULTGTUB = 14
  FULLNAME = 15
  with open(filename, 'rb') as nutrientCSV:
    nutrientReader = csv.reader(nutrientCSV)
    next(nutrientReader, None)
    for row in nutrientReader:
      weight = {'lb':{'less':{'linear':float(row[WEIGHTLTLB])},'great':{'linear':float(row[WEIGHTGTLB])}},'ub':{'less':{'linear':float(row[WEIGHTLTUB])},'great':{'linear':float(row[WEIGHTGTUB])}}}
      default = {'lb':{'less':{'linear':float(row[DEFAULTLTLB])},'great':{'linear':float(row[DEFAULTGTLB])}},'ub':{'less':{'linear':float(row[DEFAULTLTUB])},'great':{'linear':float(row[DEFAULTGTUB])}}}
      nutrientDict[int(row[ID])] = Nutrient(row[FULLNAME],row[UNIT],float(row[LB]),float(row[UB]),float(row[IDEAL]),int(row[ID]),0,bool(int(row[ACCOUNTFOR])), weight, default )
  return nutrientDict

if __name__ == "__main__":
  main()