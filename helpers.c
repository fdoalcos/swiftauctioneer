#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // row
    for (int i = 0; i < height; i++)
    {
        // column
        for (int j = 0; j < width; j++)
        {
            float blue = image[i][j].rgbtBlue;
            float green = image[i][j].rgbtGreen;
            float red = image[i][j].rgbtRed;

            int average = round((blue + green + red) / 3);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = (.393 * originalRed) + (.769 * originalGreen) + (.189 * originalBlue);
            int sepiaBlue = (.349 * originalRed) + (.686 * originalGreen) + (.168 * originalBlue);
            int sepiaGreen = (.272 * originalRed) + (.534 * originalGreen) + (.131 * originalBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            sepiaRed = image[i][j].rgbtRed;
            sepiaGreen = image[i][j].rgbtGreen;
            sepiaBlue = image[i][j].rgbtBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j ++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //copy of image
    RGBTRIPLE temp = image[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            int totalRed, totalBlue, totalGreen;
            totalRed, totalBlue, totalGreen = 0;
            float counter = 0.00;

            for (int x = -1; x < 2, x++)
            {
                for (int y = -1; x < 2; i++)
                {
                    int currentX = i + x;
                    int currentY = j = y;

                    if (currentX  < 0 || currentX > (height - 1) || currentY < 0 || currentY > (height - 1))
                    {
                        continue;
                    }
                    totalRed += image[currentX][currentY].rgbtRed;
                    totalGreem += image[currentX][currentY].rgbtGreen;
                    totalBlue += image[currentX][currentY].rgbtBlue;

                    counter++;
                }

                temp[i][j].rgbtRed = round(totalRed / counter);
                temp[i][j].rgbtGreen = round(totalGreen / counter);
                temp[i][j].rgbtBlue = round(totalBlue / counter);
            }
        }
    }
    return;
}
