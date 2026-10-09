"""
S-14: Safe Cost per Unit Calculator
Divides total cost by units, with a prepared plan for units being 0.
Try units = 0, then units = 4.
"""

total_cost = 1200
units = 0

try:
    cost_per_unit = total_cost / units
    print(f"Cost per unit: {cost_per_unit}")
except ZeroDivisionError:
    print("Can not work out cost per unit: units is 0.")
