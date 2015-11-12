import random
import requests
import json
import time
import csv
from classes.snapshot import Snapshot
from classes.nutrient import Nutrient
from classes.day import Day
from classes.food import Food

api_key = "mgj10CavRUNan0tGpl316nAdfq2AwFptv5HVyLAc"

def getResponse ( url ):
  r = requests.get(url)
  response = json.loads(r.text)
  return response

def calculateFood ( id , day):
  response = getResponse("http://api.nal.usda.gov/ndb/reports/?ndbno=" + str(id) + "&type=f&format=json&api_key=" + api_key)
  nutrients = response["report"]["food"]["nutrients"]
  food = response["report"]["food"]
  newFood = Food(id, food["name"], None, None, food["fg"])
  day.foods[newFood.id] = newFood
  newScore = 0

  #nutrients is a list
  for nutrient in nutrients:
    if nutrient["nutrient_id"] in day.nutrients:
      day.nutrients[nutrient["nutrient_id"]].value = day.nutrients[nutrient["nutrient_id"]].value + float(nutrient["value"])
      newScore += day.nutrients[nutrient["nutrient_id"]].calculateScore("linear")
  day.score = newScore
  tempSnapShot = Snapshot(day.nutrients,day.foods,day.score)
  return tempSnapShot

def getFoodForNutrient( nutrient ):
  response = getResponse("http://api.nal.usda.gov/ndb/nutrients/?format=json&api_key="+ api_key +"&nutrients="+ str(nutrient.id) +"&sort=c")
  foods = response["report"]["foods"]
  #before this call is where you could make it be random / select certain food group
  return foods

def main():
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
  with open('nutrients.csv', 'rb') as nutrientCSV:
    nutrientReader = csv.reader(nutrientCSV)
    next(nutrientReader, None)
    for row in nutrientReader:
      weight = {'lb':{'less':{'linear':float(row[WEIGHTLTLB])},'great':{'linear':float(row[WEIGHTGTLB])}},'ub':{'less':{'linear':float(row[WEIGHTLTUB])},'great':{'linear':float(row[WEIGHTGTUB])}}}
      default = {'lb':{'less':{'linear':float(row[DEFAULTLTLB])},'great':{'linear':float(row[DEFAULTGTLB])}},'ub':{'less':{'linear':float(row[DEFAULTLTUB])},'great':{'linear':float(row[DEFAULTGTUB])}}}
      nutrientDict[int(row[ID])] = Nutrient(row[FULLNAME],row[UNIT],float(row[LB]),float(row[UB]),float(row[IDEAL]),int(row[ID]),0,bool(int(row[ACCOUNTFOR])), weight, default )
  today = Day(time.strftime("%x"), nutrientDict, {},0, None)
  for name, nutrient in nutrientDict.iteritems():
    while nutrient.accountFor and ( nutrient.value < nutrient.lb ):
      #get list of all foods for nutrient
      food = getFoodForNutrient( nutrient )
      today.snapshots.append(calculateFood(food[random.randint(1, 40)]["ndbno"], today))
  print today

if __name__ == "__main__":
      main()