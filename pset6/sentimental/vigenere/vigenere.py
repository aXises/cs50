import sys


def getShift(c):
    if(c.isupper()):
        return ord(c) - 65
    else:
        return ord(c) - 97


def shiftChar(shift, c):
    if(c.isupper()):
        if(ord(c) + shift <= 90):
            return chr(ord(c) + shift)
        else:
            return chr(ord(c) + shift - 90 + 65 - 1)

    else:
        if(ord(c) + shift <= 122):
            return chr(ord(c) + shift)
        else:
            return chr(ord(c) + shift - 122 + 97 - 1)


def main(argc, argv):
    if(argc != 2):
        exit(1)
    key = argv[argc - 1]
    for i in range(0, len(key)):
        if(not key[i].isalpha()):
            exit(1)
    plaintext = input("plaintext: ")
    print("ciphertext: ", end="")
    j = 0
    for i in range(0, len(plaintext)):
        if(plaintext[j].isalpha()):
            shift = getShift(key[j % len(key)])
            print(shiftChar(shift, plaintext[i]), end="")
            j += 1
        else:
            if(plaintext[i] == " "):
                print(" ", end="")
            else:
                print(plaintext[i], end="")
    print("")


main(len(sys.argv), sys.argv)
