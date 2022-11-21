try:
    with open("adat.txt", "r") as f:
        for line in f:
            print(line.strip(), end=" ")
except FileNotFoundError as e:
    print("A file nem található: " + e.filename)
