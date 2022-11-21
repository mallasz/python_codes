import math


def ticket_counter(base, age, distance):
    """calculate the ticket price
base: base price for regular ticket for 100 kms
age: passenger's age
distance: distance in kms
"""
    if age < 6 or age >= 65:
         return 0
    elif age < 18:
        return ((math.ceil(distance / 100) * base)) / 2
    else:
        return (math.ceil(distance / 100) * base)
