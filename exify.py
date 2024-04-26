#!/usr/bin/env python3

import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

# Helper function
def create_google_maps_url(gps_coords):
    dec_deg_lat = convert_decimal_degrees(
        float(gps_coords["lat"][0]),
        float(gps_coords["lat"][1]),
        float(gps_coords["lat"][2]),
        gps_coords["lat_ref"]
    )
    dec_deg_lon = convert_decimal_degrees(
        float(gps_coords["lon"][0]),
        float(gps_coords["lon"][1]),
        float(gps_coords["lon"][2]),
        gps_coords["lon_ref"]
    )
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"

def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees



cwd = os.getcwd()
os.chdir("/home/eyob/Desktop/DF")
files = os.listdir()

output_choice = input("How do you want to receive the output:\n\n1 - File\n2 - Terminal\nEnter choice here: ")

if len(files) == 0:
    print("No files found in the /home/eyob/Desktop/DF folder.")
    exit()

for file in files:
    try:
        image = Image.open(file)
        print(f"_______________________________________________________________{file}_______________________________________________________________")
        gps_coords = {}
        if image._getexif() == None:
            print(f"{file} contains no EXIF data.")
        else:
            for tag, value in image._getexif().items():
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        print(f"{GPSTAGS.get(key)} - {val}")
                        if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val   
                else:
                    print(f"{tag_name} - {value}")
            if gps_coords:
                print(create_google_maps_url(gps_coords))
    except IOError:
        print("File format not supported!")

os.chdir(cwd)
