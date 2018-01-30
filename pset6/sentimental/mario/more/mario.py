height = None

while (True):
    try:
        height = int(input("Height: "))
        if (height < 0 or height > 23):
            pass
        else:
            break
    except ValueError:
        pass
i = 0
for i in range(0, height):
    j = height
    while (j > 0):
        if (i + 1 > j - 1):
            print("#", end="")
        else:
            print(" ", end="")
        j -= 1
    print("  ", end="")
    for k in range(0, i + 1):
        print("#", end="")
    print("\n", end="")
