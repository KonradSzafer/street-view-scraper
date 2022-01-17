import os
from pathlib import Path
import time
import json
import csv

import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import webbrowser
import pyautogui
import pyperclip
import pyscreenshot as ImageGrab
import tkinter as tk


def drag_mouse(start_x, start_y, end_x, end_y, seconds=1):

    pyautogui.mouseDown(button='left',
                        x=start_x,
                        y=start_y)

    pyautogui.dragTo(end_x, end_y,
                    seconds,
                    button='left')


def get_graphics_location(image_path, confidence=0.8, wait_time=0.1):

    for _ in range(50):
        try:
            icon_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            icon_location = pyautogui.center(icon_location)
            if icon_location.x != None and icon_location.y != None:
                break
        except:
            time.sleep(wait_time)

    return icon_location


def get_street_view_url(longitude, latitiude, height=10):
    url = 'https://www.google.pl/maps/@{0},{1},{2}z'
    url = url.format(longitude, latitiude, height)
    return url


def get_street_view_image():

    img_width, img_height = 800, 800
    start_x, start_y = 600, 130
    end_x = start_x + img_width
    end_y = start_y + img_height

    img = pyautogui.screenshot()
    img = img.crop((start_x, start_y, end_x, end_y))
    img = np.asarray(img)
    return img


def get_street_view_images(longitude_range, latitude_range):

    longitude = np.random.uniform(*longitude_range)
    latitude = np.random.uniform(*latitude_range)

    # open google maps url
    url = get_street_view_url(longitude, latitude)
    webbrowser.open_new(url)

    # move human icon in the middle of the map
    time.sleep(1)
    icon_location = get_graphics_location('graphics\human_icon.png')
    time.sleep(1)

    # try to drop human on street
    screen_middle_x = root.winfo_screenwidth() / 2
    screen_middle_y = root.winfo_screenheight() / 2
    for i in range(10):
        # drop wherever in middle of the screen
        drop_x = int(screen_middle_x + np.random.randint(-200, 200))
        drop_y = int(screen_middle_y + np.random.randint(-200, 200))

        drag_mouse( start_x=icon_location.x, start_y=icon_location.y,
                    end_x=drop_x,
                    end_y=drop_y,
                    seconds=1)

        # check if street is fully loaded
        time.sleep(2)
        bar_location = get_graphics_location('graphics/side_bar.png')
        if bar_location != None:
            break

    # unable to drop on street
    if bar_location == None:
        pyautogui.hotkey('ctrl', 'F4')
        return 0

    # get screen shots of street
    # ? check if screenshot of screen is dark or blurry
    # time.sleep(3) # depends on the internet
    images = {}
    images_count = 7
    for i in range(images_count):

        # get url data
        time.sleep(0.5)
        url_location = get_graphics_location('graphics/url_image.png')

        pyautogui.click(x=url_location.x, #+50
                        y=url_location.y,
                        clicks=3)

        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.05)
        url_data = pyperclip.paste()

        # take screen shot
        img = get_street_view_image()
        images[url_data] = img

        # move camera
        if i < images_count-1:
            drag_mouse( start_x=400, start_y=500,
                        end_x=1000, end_y=500,
                        seconds=0.4)

    # close current tab
    pyautogui.hotkey('ctrl', 'F4')
    return images


if __name__ == '__main__':

    # settings
    region_name = 'switzerland'
    places_count = 1

    # subregion format: name, (min_longitude, max_longitude, min_latitude, max_latitude)
    subregions = []
    with open('coords.json') as coords_file:
        subregions = json.load(coords_file)[region_name]

    working_dir = os.getcwd()
    images_foldername = working_dir + '/data/' + region_name + '/'
    geodata_foldername = working_dir + '/data/' + region_name + '_coor/'

    # create necessary folders and files
    Path(images_foldername).mkdir(parents=True, exist_ok=True)
    Path(geodata_foldername).mkdir(parents=True, exist_ok=True)

    f = open(geodata_foldername + 'data.csv', 'a', newline='')
    writer = csv.writer(f)

    root = tk.Tk()

    images_count = 0
    start_time = time.time()
    for i in range(places_count):

        # get longitude and latitude ranges
        subregion_name, coords = random.choice(list(subregions.items()))
        longitude_range = (coords[0], coords[1])
        latitude_range = (coords[2], coords[3])

        # rand location and get images
        results = get_street_view_images(longitude_range, latitude_range)
        images_count += len(results)
        if results == 0:
            continue

        for url, image in results.items():
            # plt.imshow(image)
            # plt.show()

            # create unique image name based on geodata
            image_name = url.replace('https://www.google.pl/maps/@', '')
            image_name = image_name.split('/data')[0]
            image_name = image_name.replace(',', '-')
            image_name = image_name.replace('.', '_')

            # link image name with url
            row = [image_name, subregion_name, url]
            writer.writerow(row)

            # save images
            image = Image.fromarray(image)
            image.save(images_foldername + image_name + '.png')

    f.close()
    end_time = time.time()

    print('Duration: %ds' % int(end_time - start_time))
    print('Scraped images: %d' % images_count)
