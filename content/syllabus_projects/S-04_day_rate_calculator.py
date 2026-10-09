"""
S-04 — Freelance Day-Rate Calculator
Hours worked x hourly rate, minus a deduction, equals what actually lands in
your account.
"""

hourly_rate = 50
hours_worked = 8

total_cost = hourly_rate * hours_worked

deduction_rate = 0.1
deduction = total_cost * deduction_rate
final_cost = total_cost - deduction

print("Hours worked:", hours_worked)
print("Hourly rate: RM", hourly_rate)
print("Total before deduction: RM", total_cost)
print("Deduction (10%): RM", deduction)
print("Final amount: RM", final_cost)
