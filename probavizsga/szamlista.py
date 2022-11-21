def input_reader(text, error_text):
    """reads an integer
    text: question to be printed to the user
    error_text: text to print, that the given input is not an integer"""
    while True:
        x = input(text)
        try:
            x = int(x)
            return x
        except ValueError:
            print(error_text)


def between(a, b):
    """
    Returns values between a and b including b
    :param a: int
    :param b: int
    :return: list of values between a and b including b
    """
    return list(range(min(a, b), max(a, b) + 1))


number1 = input_reader("Add meg az egyik egész számot: ", "Ez nem egy egész szám, adj meg egy egész számot!")
number2 = input_reader("Add meg a másik egész szamot: ", "Ez nem egy egész szám, adj meg egy egész számot!")

print(between(number1, number2))
