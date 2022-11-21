def fuel_consumption(consumption_extra_urban, consumption_urban, distance_extra_urban, distance_urban, fuel_price):
    """calculate the consumption
    consumption_extra urban: the consumption on highway in L/100km
    consumption_urban: the consumption in city in L/100 km
    distance_extra_urban: distance travelled on highway in kms
    distance_urban: distance travelled in city
    fuel_price: price of the fuel
    """
    consumption_oneway = consumption_extra_urban / 100 * distance_extra_urban + consumption_urban / 100 * distance_urban
    consumption_return = consumption_oneway * 2
    fuel_costs_oneway = consumption_oneway * fuel_price
    fuel_costs_return = fuel_costs_oneway * 2

    return (consumption_oneway, consumption_return, fuel_costs_oneway, fuel_costs_return)


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


consumption_oneway, consumption_return, fuel_costs_oneway, fuel_costs_return = fuel_consumption(7, 9, 170, 35, 480)

print(
    f'fogyasztás odaúton: {consumption_oneway} liter\nfogyasztás oda-vissza: {consumption_return} liter \nbenzinköltség odaúton: {fuel_costs_oneway:.0f} Ft. \nbenzinköltség oda-vissza: {fuel_costs_return:.0f} Ft.')

consumption_extra_urban = input_reader("Add meg az országúti fogyasztást: ",
                                       "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot",
                                       lambda x: x >= 0)
consumption_urban = input_reader("Add meg a városi fogyasztást: ",
                                 "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot", lambda x: x >= 0)
distance_extra_urban = input_reader(""
                                    "Add meg az országút hosszát: ",
                                    "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot", lambda x: x >= 0)
distance_urban = input_reader("Add meg a városi út hosszát: ",
                              "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot", lambda x: x >= 0)
fuel_price = input_reader("Add meg a benzin árát: ", "Ez nem egy pozitív egész szám, adj meg egy pozitív egész számot",
                          lambda x: x >= 0)

consumption_oneway, consumption_return, fuel_costs_oneway, fuel_costs_return = fuel_consumption(consumption_extra_urban,
                                                                                                consumption_urban,
                                                                                                distance_extra_urban,
                                                                                                distance_urban,
                                                                                                fuel_price)

print(
    f'fogyasztás odaúton: {consumption_oneway:.2f} liter\n'
    f'fogyasztás oda-vissza: {consumption_return:.2f} liter \n'
    f'benzinköltség odaúton: {fuel_costs_oneway:.0f} Ft. \n'
    f'benzinköltség oda-vissza: {fuel_costs_return:.0f} Ft.')
