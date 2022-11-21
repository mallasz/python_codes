summa = 0
number_of_items = 0

print("Add meg a 20-nál kisebb számokat:")

while True:
    try:
        i = int(input())
        if i >= 20:
            break
    except:
        continue
    number_of_items += 1
    summa = summa + i

if number_of_items > 0:
    print(f'Számok összege: {summa}, Számok átlaga: {summa / number_of_items:.2f}')
else:
    print("Nem lett 20-nál kisebb szám megadva")
