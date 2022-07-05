#! /usr/bin/python3
from itertools import combinations_with_replacement, product
from math import prod
import numpy as np

print("Hello, world!")

resPerBranch = int(input(f"Enter max number of resistors per branch: "))

print("Building resistance combinations")

baseVals = [10, 22, 47]

rCombs = []

for i in range(2, resPerBranch + 1):
  for c in combinations_with_replacement(baseVals, i):
    rCombs.append(c)

serCombs = []
parCombs = []

for c in rCombs:
  serCombs.append((*c, sum(c)))
  parCombs.append((*c, 1 / (sum([1 / v for v in c]))))

finalVals = [(a, a) for a in baseVals] + serCombs + parCombs
# First value in the tuple is the "top" resistor branch
# Second is "bottom" resistor branch
ratios = [(a[0], a[1], a[1] / (a[0] + a[1])) for a in product([i[-1] for i in finalVals], repeat=2)]

inputVoltage = float(input("Input voltage: "))
outputVoltage = float(input("Output voltage: "))

if outputVoltage > inputVoltage:
  print("Output voltage cannot be greater than input voltage")
  quit()

desiredRatio = outputVoltage / inputVoltage
lst = np.asarray([a[2] for a in ratios])
bestRatio = ratios[(np.abs(lst - desiredRatio)).argmin()]

print(f"Desired voltage ratio: {desiredRatio}")
print(f"Best implemented ratio: {bestRatio[2]}")
print(f"Output voltage will be reached at Vin = {round(outputVoltage / bestRatio[2], 3)}V")
print()

for v in baseVals:
  if v == bestRatio[0]:
    print(f"Top resistor network: one resistor: {v}")
  if v == bestRatio[1]:
    print(f"Bottom resistor network: one resistor: {v}")

for v in serCombs:
  if v[-1] == bestRatio[0]:
    print(f"Top resistor network: series combination: {v[:-1]} = {bestRatio[0]}")
  if v[-1] == bestRatio[1]:
    print(f"Bottom resistor network: series combination: {v[:-1]} = {bestRatio[1]}")

for v in parCombs:
  if v[-1] == bestRatio[0]:
    print(f"Top resistor network: parallel combination: {v[:-1]} = {bestRatio[0]}")
  if v[-1] == bestRatio[1]:
    print(f"Bottom resistor network: parallel combination: {v[:-1]} = {bestRatio[1]}")
  
