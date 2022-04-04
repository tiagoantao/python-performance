import csv
import os
import sys

data_dir = sys.argv[1]

# https://www.ncei.noaa.gov/data/global-hourly/archive/csv/2021.tar.gz


def get_locations(file_name):
    with open(file_name, "rt") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            station = row[header.index("STATION")]
            lat = row[header.index("LATITUDE")]
            lon = row[header.index("LONGITUDE")]
            return station, (lat, lon)


def dump_all_locations(data_dir, w):
    for file_name in os.listdir(data_dir):
        station, (lat, lon) = get_locations(f"{data_dir}/{file_name}")
        w.write(f"{station},{lat},{lon}\n")


with open("locations.csv", "wt") as w:
    dump_all_locations(data_dir, w)

