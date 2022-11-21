from S11_calculator import cylinder_curved_surface


def input_reader(text, error_text, condition_function):
    """reads a float that satisfied the given condition
    text: question to be printed to the user
    error_text: text to print, that the given input is a float, but does not satisfy the given condition
    condition_function: function that is given a float and returns boolean, check if the number satisfy the additional condition
    """
    while True:
        x = input(text)
        try:
            x = float(x)
            if condition_function(x):
                return x
            else:
                print(error_text)
        except ValueError as e:
            print("Nem egy szám került megadásra")


cylinder_radius = input_reader("Add meg a henger sugarát: ", "Nem pozitív számot adtál meg", lambda x: x > 0)
cylinder_height = input_reader("Add meg a henger magasságát: ", "Nem pozitív számot adtál meg", lambda x: x > 0)

print(cylinder_curved_surface(cylinder_radius, cylinder_height))
