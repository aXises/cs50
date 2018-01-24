#include <stdio.h>
#include <cs50.h>
#include <math.h>

long long getIndexRev (long long number, int index)
{
    long long divNumber = number / pow(10, index);
    return divNumber % 10;
}

int getLength (long long number)
{
    float newNum = number;
    int length = 0;
    while (newNum >= 1)
    {
        length++;
        newNum = newNum / 10;
    };
    return length;
};

int main (void)
{
    long long number = get_long_long("Number: ");
    int initVal, val, doubleVal, sumOdds, sumEven;
    while (!number)
    {
        get_long_long("Number: ");
    }
    sumOdds = 0;
    sumEven = 0;
    for (int i = 0; i < getLength(number); i++)
    {
        val = getIndexRev(number, i);
        doubleVal = val * 2;
        if ( i % 2 != 0 )
        {
            if (getLength(doubleVal)  <= 1)
            {
                sumOdds += doubleVal;
            }
            else
            {
                for (int j = 0; j < getLength(doubleVal); j++)
                {
                    sumOdds += getIndexRev(doubleVal, j);
                };
            }
        }
        else
        {
            sumEven += val;
        }
    }
    if (getIndexRev(sumOdds + sumEven, 0) != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        initVal = getIndexRev(number, getLength(number) - 1);
        //printf("%i\n", initVal);
        switch (initVal)
        {
            case 3:
                printf("AMEX\n");
                break;
            case 4:
                printf("VISA\n");
                break;
            case 5:
                printf("MASTERCARD\n");
                break;
            default:
                printf("INVALID\n");
                break;
        }
    }
};

