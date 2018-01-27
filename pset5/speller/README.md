# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

From the dictionary, it means: "an invented long word said to mean a lung disease caused by inhaling very fine ash and sand dust.".

## According to its man page, what does `getrusage` do?

Gets the resource usage of the program.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Calculate has a return value which is stored in 'time_size', therefore 'before' and 'after' do not need their values changed.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

The loop will keep getting the next character until 'c != EOF' or end of file. If the character is not a digit, it is appended to a array, but if a space is detected then a string terminator is appended to indicate the end of a word before it is passed to check.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

fscanf may not check if there is a digit in the character.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So the arguments may not be modified during the execution. This saves memory as the value does not need to be loaded in memory.
