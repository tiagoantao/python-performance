import collections
import csv
import os

import requests

# stations = sys.argv[1].split(",")
# years = [int(year) for year in sys.argv[2].split("-")]
# start_year = years[0]
# end_year = years[1]

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


# pandas would be more standard
def get_file_temperatures(file_name):
    with open(file_name, "rt") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            station = row[header.index("STATION")]
            # date = datetime.datetime.fromisoformat(row[header.index('DATE')])
            tmp = row[header.index("TMP")]
            temperature, status = tmp.split(",")
            if status != "1":
                continue
            temperature = int(temperature) / 10
            yield temperature


def get_all_temperatures(stations, start_year, end_year):
    temperatures = collections.defaultdict(list)
    for station in stations:
        for year in range(start_year, end_year + 1):
            for temperature in get_file_temperatures(TEMPLATE_FILE.format(station=station, year=year)):
                temperatures[station].append(temperature)
    return temperatures


stations = ['01044099999']
start_year = 2005
end_year = 2021
download_all_data(stations, start_year, end_year)
all_temperatures = get_all_temperatures(stations, start_year, end_year)

first_all_temperatures = all_temperatures[stations[0]]
print(len(first_all_temperatures), max(first_all_temperatures), min(first_all_temperatures))

%timeit (-10.7 in first_all_temperatures)
%timeit (-100 in first_all_temperatures)

set_first_all_temperatures = set(first_all_temperatures)
print(len(set_first_all_temperatures))

%timeit (-10.7 in set_first_all_temperatures)
%timeit (-100 in set_first_all_temperatures)


a_list_range = list(range(100000))
a_set_range = set(a_list_range)

%timeit 50000 in a_list_range
%timeit 50000 in a_set_range
%timeit 500000 in a_list_range
%timeit 500000 in a_set_range
