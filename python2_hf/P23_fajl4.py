try:
    with open("adat.txt", "r") as f:
        lst = f.readlines()

    with open("eredmeny.txt", "w") as file:
        file.writelines(lst)

except FileNotFoundError as e:
    print("A file nem található: " + e.filename)
