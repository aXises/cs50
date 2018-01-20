# Questions

## What's `stdint.h`?

A header file that allows programmers to specifiy exact width integer types.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

A fixed size integer reduces memory issues when running the program on different envrionments.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE is 1 byte, DWORD is 4 bytes, LONG is 4 bytes and WORD is 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

'BM'.

## What's the difference between `bfSize` and `biSize`?

bfSize is the size of the entire file, biSize is only the size of BITMAPINFOHEADER.

## What does it mean if `biHeight` is negative?

The origin of the bitmap starts from the bottom.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the file does not exist.

## Why is the third argument to `fread` always `1` in our code?

To read one element at a time.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3
## What does `fseek` do?

Update the file position indicator.

## What is `SEEK_CUR`?

Find the current position which has been read up to in the file.
