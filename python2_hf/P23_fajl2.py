try:
    with open("adat.txt", "r") as f:
        lst = f.readlines()
    print(" ".join([line.strip() for line in lst]))
except FileNotFoundError as e:
    print("A file nem található: " + e.filename)
