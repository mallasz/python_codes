def leapyear(year):
    if year % 400 == 0:
        return True
    elif year % 4 == 0 and year % 100 != 0:
        return True
    else:
        return False

def input_reader(text, error_text):
    """reads an integer
    text: question to be printed to the user
    error_text: text to print, that the given input is not an integer"""
    while True:
        print(text)
        x = input()
        try:
            x = int(x)
            return x
        except:
            print(error_text)

year = input_reader("Adj meg egy évszámot: ", "Ez nem egy évszám, adj meg egy évszámot!")

if leapyear(year):
    print(f' Bevitt érték: {year} Szökőév')
else:
    print(f' Bevitt érték: {year} Nem szökőév')
