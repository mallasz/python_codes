import math


def input_reader(text, error_text, condition_function):
    """reads an integer that satisfied the given condition
    text: question to be printed to the user
    error_text: text to print, that the given input is an integer, but does not satisfy the given condition
    condition_function: function that is given an integer and returns boolean, check if the number satisfy the additional condition
    """
    while True:
        print(text)
        x = input()
        try:
            x = int(x)
            if condition_function(x):
                return x
            else:
                print(error_text)
        except:
            print("Nem egy szám került megadásra")


def ticket_price(age, distance):
    """calculate the ticket price
    age: passenger's age
    distance: distance in kms
    """
    if age < 6 or age >= 65:
        return 0
    elif age < 18:
        return ((math.ceil(distance / 100) * 350)) / 2
    else:
        return (math.ceil(distance / 100) * 350)


age = input_reader("Add meg az életkorodat: ", "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot",
                   lambda x: x >= 0)
distance = input_reader("Add meg az utazási távolságot: ",
                        "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot", lambda x: x >= 0)

print(f'jegyár: {ticket_price(age, distance):.0f}')

