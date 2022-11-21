try:
    with open("adat.txt", "r") as f:
        with open("eredmeny.txt", "w") as file:
            for line in f:
                file.write(line)
except FileNotFoundError as e:
    print("A file nem található: " + e.filename)
