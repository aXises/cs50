number = str(input("Number: "))
while(not number):
    number = str(input("Number: "))
i = 0
sumEven = 0
sumOdd = 0
for i in range(len(number), 0):
    val = int(number[i])
    if(i % 2 != 0):
        if(val * 2 < 10):
            sumOdd += val * 2
        else:
            val = str(val * 2)
            j = 0
            for j in range(0, len(val)):
                sumOdd += int(val[j])
    else:
        sumEven += val
total = str(sumOdd + sumEven)
if(int(total[len(total) - 1]) != 0):
    print("INVALID")
else:
    initVal = int(number[0])
    if (initVal == 3):
        print("AMEX")
    elif (initVal == 4):
        print("VISA")
    elif (initVal == 5):
        print("MASTERCARD")
    else:
        print("INVALID")
