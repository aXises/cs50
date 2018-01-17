// Helper functions for music

#include <cs50.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator = fraction[0] - 48;
    int denominator = fraction[2] - 48;
    return numerator * (8 / denominator);
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    const int initialHz = 440;
    int hertz = initialHz;
    float shift = 0;
    char acc, octave = note[1], noteChar = note[0];
    bool accidental = false;
    if (note[1] == '#' || note[1] == 'b')
    {
        acc = note[1];
        octave = note[2];
        accidental = true;
    }
    if (octave != '4')
    {
        hertz = hertz * pow(2, (octave - 48 - 4));
    }
    if (accidental)
    {
        if (acc == '#')
        {
            shift++;
        }
        else
        {
            shift--;
        }
    }
    if (noteChar != 'A')
    {
        switch (noteChar)
        {
            case 'B':
                shift += 2;
                break;
            case 'C':
                shift -= 9;
                break;
            case 'D':
                shift -= 7;
                break;
            case 'E':
                shift -= 5;
                break;
            case 'F':
                shift -= 4;
                break;
            case 'G':
                shift -= 2;
                break;
            default:
                printf("err\n");
                break;
        }
    }

    return round(hertz * pow(2, shift / 12.0));
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strlen(s) == 0)
    {
        return true;
    }
    return false;
}
