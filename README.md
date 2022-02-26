# street-view-scraper

This script was created to easily scrape Google Street View images without using Google API.\
This can be done with Google Maps as the URL can be fully generated from the coordinates, unlike Google Earth as it requires additional code in the URL.\
It uses Google Maps to find the location and Google Street View to take screenshots.
Demonstration video: https://youtu.be/LWvcBPBZtws

## How it works

In the first step, the script loads the coords.json file. This file contains regions with subregions assigned to them, and each subregion contains coordinate ranges.\
Based on the given longitude and latitude values, draws the coordinates of where the screenshots were taken.\
Subregions and sites are generated with a uniform distribution.

In the next step, it builds a Google Maps URL based on the coordinates and passes it to the browser.\
When the page loads, it attempts to place a yellow human icon on a road or location.\
After a failure, it tries to drop it again, and after a certain number of attempts, it draws the location all over again.

In the next step, screenshots are taken, after which the script retrieves the current URL and rotates the view. The sequence is repeated a specified number of times.

Each screenshot is checked for blur and saved only if the value of the Laplacian operator is greater than the specified value.\
The same function is used as one of the two elements to check if the site is fully loaded.

Images are saved after every sequence for place, with name based on coords.\
Images are saved after each screenshot sequence to a csv file. The file line links the image name to the subregion name and the exact URL.

At each drawn location, 6 screenshots are taken by changing directions.\
Each image has a resolution of 800x800px, and this value can be changed.\
Images are collected at 900 samples per hour, this value may be lower depending on the internet speed and urbanization of the region.

## How to run it

Install the required packages or the full conda enviroment.
Specify regions and subregions in the coords.json file.
Scraper uses icons and other browser graphics to work properly, for default browser dark mode is needed or images in grapfics folder need to be changed.
After the region and number of places are specified, everything is ready.

## Other tools

- Interactive map for searching coordinates: https://www.latlong.net/
- dataset_stats.py file checks images count for each region, to make dataset collecting easy.
