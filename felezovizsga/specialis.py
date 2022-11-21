def special_eleven(num):
    """
    checks if the number is divisible by 11 or the remainder is 1
    :param num: an integer
    :return: bool
    """
    if num % 11 == 0 or num % 11 == 1:
        return True
    else:
        return False


def read_input():
    """
    reads from terminal
    :return: None
    """
    while True:
        try:
            return int(input("Kérek egy egész számot!"))
        except ValueError:
            print("Ez nem egy egész szám!")


num = read_input()
print("Igen" if special_eleven(num) else "Nem")
