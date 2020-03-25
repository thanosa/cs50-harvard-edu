
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Ensure proper usage.
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Saves the filename passed as an argument.
    char *input_filename = argv[1];

    // Opens the input file
    FILE *input_file = fopen(input_filename, "r");

    // Validates that the input file exists.
    if (!input_file)
    {
        printf("File doesn't exist: %s\n", input_filename);
        return 1;
    }

    // Creates a buffer with size of 512 bytes.
    const int block_size = 512;
    unsigned char buffer[512];

    // Image file name increment.
    int image_counter = 0;

    // Keeps the state of the file;
    int file_is_open = 0;

    // Declater the output file here so that we can close it in the end.
    FILE *output_file;

    // Reads the file in blocks of 512 bytes.
    while (fread(buffer, 1, block_size, input_file) == block_size)
    {

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] >= 0xe0 && buffer[3] <= 0xef)
        {
            if (file_is_open == 1)
            {
                // Close the output file.
                fclose(output_file);

                // Updates the file state.
                file_is_open = 0;
            }

            // Builds the output file name.
            char image_name[sizeof "###.jpg"];
            sprintf(image_name, "%03i.jpg", image_counter++);

            // Opens the output filename.
            output_file = fopen(image_name, "w");

            // Updates the file state.
            file_is_open = 1;
        }

        if (file_is_open == 1)
        {
            // Writes the block
            fwrite(buffer, 1, block_size, output_file);
        }
    }

    if (file_is_open == 1)
    {
        // Close the output file.
        fclose(output_file);
    }

    return 0;
}
