
def increment():
    file = open("nb.txt", "r")
    nb = file.readline()
    print(nb)
    file.close()
    file = open("nb.txt", "w")
    nb = int(nb) + 1
    file.write(str(nb))
    file.close()