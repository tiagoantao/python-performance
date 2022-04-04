import array
import collections
import os
import sys

import requests

stations = sys.argv[1].split(",")
years = [int(year) for year in sys.argv[2].split("-")]
start_year = years[0]
end_year = years[1]

TEMPLATE_URL = "https://www.ncei.noaa.gov/data/global-hourly/access/{year}/{station}.csv"
TEMPLATE_FILE = "station_{station}_{year}.csv"

def download_data(station, year):
    my_url = TEMPLATE_URL.format(station=station, year=year)
    req = requests.get(my_url)
    if req.status_code != 200:
        return  # not found
    w = open(TEMPLATE_FILE.format(station=station, year=year), "wt")
    w.write(req.text)
    w.close()


def download_all_data(stations, start_year, end_year):
    for station in stations:
        for year in range(start_year, end_year + 1):
            if not os.path.exists(TEMPLATE_FILE.format(station=station, year=year)):
                download_data(station, year)


def get_all_files(stations, start_year, end_year):
    all_files = collections.defaultdict(list)
    for station in stations:
        for year in range(start_year, end_year + 1):
            f = open(TEMPLATE_FILE.format(station=station, year=year), 'rb')
            content = list(f.read())
            all_files[station].append(content)
            f.close()
    return all_files


stations = ['01044099999']
start_year = 2005
end_year = 2021
download_all_data(stations, start_year, end_year)
all_files = get_all_files(stations, start_year, end_year)

list(all_files.keys())

print(sys.getsizeof(all_files))
print(sys.getsizeof(all_files.values()))
print(sys.getsizeof(list(all_files.values())))

station_content = all_files[stations[0]]
print(len(station_content))
print(sys.getsizeof(station_content))
print(len(station_content[0]))
print(sys.getsizeof(station_content[0]))
print(type(station_content[0]))
print(station_content[0][0])

print(sys.getsizeof('text'))
print(sys.getsizeof('longer text'))
print(sys.getsizeof(['text']))
print(sys.getsizeof(['longer text']))

print(sys.getsizeof(station_content[0][0]))
print(type(station_content[0][0]))
id(station_content[0][2])

single_file_data = station_content[0]
all_ids = set()
for entry in single_file_data:
    all_ids.add(id(entry))
print(len(all_ids))


single_file_str_list = [chr(i) for i in single_file_data]
print(sys.getsizeof(single_file_str_list[0]))

single_file_str = ''.join(single_file_str_list)
print(sys.getsizeof(single_file_str))


def get_all_files_clean(stations, start_year, end_year):
    all_files = collections.defaultdict(list)
    for station in stations:
        for year in range(start_year, end_year + 1):
            f = open(TEMPLATE_FILE.format(station=station, year=year), 'rb')
            content = f.read()
            all_files[station].append(content)
            f.close()
    return all_files


all_files_clean = get_all_files_clean(stations, start_year, end_year)


single_file_data = all_files_clean[stations[0]][0]
print(type(single_file_data))
print(sys.getsizeof(single_file_data))


len(single_file_data)
(len(single_file_data) + 1) // 2
