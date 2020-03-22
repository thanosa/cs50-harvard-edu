#include "helpers.h"
#include "math.h"
#include <stdbool.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int intensity = round((image[y][x].rgbtBlue + image[y][x].rgbtGreen + image[y][x].rgbtRed) / (float)3);
            image[y][x].rgbtBlue = intensity;
            image[y][x].rgbtGreen = intensity;
            image[y][x].rgbtRed = intensity;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int mirror = width - x - 1;
            temp[y][mirror].rgbtBlue = image[y][x].rgbtBlue;
            temp[y][mirror].rgbtGreen = image[y][x].rgbtGreen;
            temp[y][mirror].rgbtRed = image[y][x].rgbtRed;
        }

        for (int x = 0; x < width; x++)
        {
            image[y][x].rgbtBlue = temp[y][x].rgbtBlue;
            image[y][x].rgbtGreen = temp[y][x].rgbtGreen;
            image[y][x].rgbtRed = temp[y][x].rgbtRed;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary copy as we cannot put the results directly to the original image,
    // due to interference.
    RGBTRIPLE average[height][width];

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            // Neighborhood squares: on the cross
            int selfY = y;
            int selfX = x;

            int leftY = y;
            int leftX = x - 1;

            int rightY = y;
            int rightX = x + 1;

            int topY = y - 1;
            int topX = x;

            int botY = y + 1;
            int botX = x;

            // Neigborhood squares: on the diagonal
            int topLeftY = topY;
            int topLeftX = leftX;

            int topRightY = topY;
            int topRightX = rightX;

            int botRightY = botY;
            int botRightX = rightX;

            int botLeftY = botY;
            int botLeftX = leftX;

            // Control variables
            bool hasSelf = true;
            bool hasTop = y > 0;
            bool hasBot = y < height - 1;
            bool hasLeft = x > 0;
            bool hasRight = x < width - 1;

            // Initialization
            int blue = 0;
            int green = 0;
            int red = 0;

            int count = 0;

            // Temprorary variables
            int tmpY;
            int tmpX;

            // The square itself.
            if (hasSelf)
            {
                tmpY = selfY;
                tmpX = selfX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a top square.
            if (hasTop)
            {
                tmpY = topY;
                tmpX = topX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a top-rigth square.
            if (hasTop && hasRight)
            {
                tmpY = topRightY;
                tmpX = topRightX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a right square.
            if (hasRight)
            {
                tmpY = rightY;
                tmpX = rightX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a bottom-right square.
            if (hasBot && hasRight)
            {
                tmpY = botRightY;
                tmpX = botRightX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a bottom square.
            if (hasBot)
            {
                tmpY = botY;
                tmpX = botX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a bottom-left square.
            if (hasBot && hasLeft)
            {
                tmpY = botLeftY;
                tmpX = botLeftX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a bottom-left square.
            if (hasLeft)
            {
                tmpY = leftY;
                tmpX = leftX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a bottom-left square.
            if (hasTop && hasLeft)
            {
                tmpY = topLeftY;
                tmpX = topLeftX;

                blue += image[tmpY][tmpX].rgbtBlue;
                green += image[tmpY][tmpX].rgbtGreen;
                red += image[tmpY][tmpX].rgbtRed;

                count++;
            }

            // Check if there is a bottom-left square.
            average[selfY][selfX].rgbtBlue = round(blue / (float) count);
            average[selfY][selfX].rgbtGreen = round(green / (float) count);
            average[selfY][selfX].rgbtRed = round(red / (float) count);
        }
    }

    // Copy the temporary image to the original one.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x].rgbtBlue = average[y][x].rgbtBlue;
            image[y][x].rgbtGreen = average[y][x].rgbtGreen;
            image[y][x].rgbtRed = average[y][x].rgbtRed;
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary copy as we cannot put the results directly to the original image,
    // due to interference.
    RGBTRIPLE temp[height][width];

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            // Neighborhood squares: on the cross
            int selfY = y;
            int selfX = x;

            int leftY = y;
            int leftX = x - 1;

            int rightY = y;
            int rightX = x + 1;

            int topY = y - 1;
            int topX = x;

            int botY = y + 1;
            int botX = x;

            // Neigborhood squares: on the diagonal
            int topLeftY = topY;
            int topLeftX = leftX;

            int topRightY = topY;
            int topRightX = rightX;

            int botRightY = botY;
            int botRightX = rightX;

            int botLeftY = botY;
            int botLeftX = leftX;

            // Control variables
            bool hasSelf = true;
            bool hasTop = y > 0;
            bool hasBot = y < height - 1;
            bool hasLeft = x > 0;
            bool hasRight = x < width - 1;

            // Initialization
            int blueGy = 0;
            int greenGy = 0;
            int redGy = 0;

            int blueGx = 0;
            int greenGx = 0;
            int redGx = 0;

            // Temprorary variables
            int tmpY;
            int tmpX;

            int kernelY;
            int kernelX;

            // Check if there is a top square.
            if (hasSelf)
            {
                tmpY = selfY;
                tmpX = selfX;

                kernelY = 0;
                kernelX = 0;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            if (hasTop)
            {
                tmpY = topY;
                tmpX = topX;

                kernelY = -2;
                kernelX = 0;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a top-rigth square.
            if (hasTop && hasRight)
            {
                tmpY = topRightY;
                tmpX = topRightX;

                kernelY = -1;
                kernelX = 1;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a right square.
            if (hasRight)
            {
                tmpY = rightY;
                tmpX = rightX;

                kernelY = 0;
                kernelX = 2;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a bottom-right square.
            if (hasBot && hasRight)
            {
                tmpY = botRightY;
                tmpX = botRightX;

                kernelY = 1;
                kernelX = 1;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a bottom square.
            if (hasBot)
            {
                tmpY = botY;
                tmpX = botX;

                kernelY = 2;
                kernelX = 0;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a bottom-left square.
            if (hasBot && hasLeft)
            {
                tmpY = botLeftY;
                tmpX = botLeftX;

                kernelY = 1;
                kernelX = -1;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a bottom-left square.
            if (hasLeft)
            {
                tmpY = leftY;
                tmpX = leftX;

                kernelY = 0;
                kernelX = -2;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Check if there is a bottom-left square.
            if (hasTop && hasLeft)
            {
                tmpY = topLeftY;
                tmpX = topLeftX;

                kernelY = -1;
                kernelX = -1;

                blueGy += image[tmpY][tmpX].rgbtBlue * kernelY;
                greenGy += image[tmpY][tmpX].rgbtGreen * kernelY;
                redGy += image[tmpY][tmpX].rgbtRed * kernelY;

                blueGx += image[tmpY][tmpX].rgbtBlue * kernelX;
                greenGx += image[tmpY][tmpX].rgbtGreen * kernelX;
                redGx += image[tmpY][tmpX].rgbtRed * kernelX;
            }

            // Calculating the rounded square root of the soebel for the three channels.
            int blueSobel = round(sqrt((float)(blueGx * blueGx + blueGy * blueGy)));
            int greenSobel = round(sqrt((float)(greenGx * greenGx + greenGy * greenGy)));
            int redSobel = round(sqrt((float)(redGx * redGx + redGy * redGy)));

            // Applies the minimum value of 255 to the result above.
            temp[selfY][selfX].rgbtBlue = blueSobel > 255 ? 255 : blueSobel;
            temp[selfY][selfX].rgbtGreen = greenSobel > 255 ? 255 : greenSobel;
            temp[selfY][selfX].rgbtRed = redSobel > 255 ? 255 : redSobel;

        }
    }

    // Copy the temporary image to the original one.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x].rgbtBlue = temp[y][x].rgbtBlue;
            image[y][x].rgbtGreen = temp[y][x].rgbtGreen;
            image[y][x].rgbtRed = temp[y][x].rgbtRed;
        }
    }

    return;
}
