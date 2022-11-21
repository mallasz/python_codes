try:
    with open("adat.txt", "r") as f:
        lst = f.readlines()
    with open("eredmeny.txt", "w") as file:
        file.write(" ".join([i.strip() for i in lst]))

except FileNotFoundError as e:
    print("A file nem található: " + e.filename)
