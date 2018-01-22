#include <stdio.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    //Check for correct arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: infile\n");
        return 1;
    }
    FILE *file = fopen(argv[argc - 1], "r");
    //Check file exists
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        fclose(file);
        return 2;
    }
    const int readSize = 512;
    unsigned char buffer[readSize];
    char jpgName[3];

    int jpgCount = 0;
    bool foundJpg = false;
    FILE *jpg;
    //Read the file
    while (fread(buffer, 1, readSize, file) == readSize)
    {
        //Start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //Close the previous jpg
            if (foundJpg)
            {
                fclose(jpg);
            }
            else
            {
                //Found first jpg
                foundJpg = true;
            }
            //Setup new jpg file
            sprintf(jpgName, "%03d.jpg", jpgCount);
            jpg = fopen(jpgName, "w");
            jpgCount++;
        }
        //Already found JPEG
        if (foundJpg)
        {
            fwrite(buffer, 1, readSize, jpg);
        }
    }
    fclose(jpg);
    fclose(file);
}