#!/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import bs4 as BeautifulSoup
import json
from time import gmtime, strftime

def clean_string(string):
    if string != None:
        string = string.replace('\r', '')
        string = string.replace(u'\xa0', '')
        if string == '':
            return None
    return string

def parse_train_data(train_number: int):
    html = urlopen('http://www.railtime.be/website/ShowTrain.aspx?l=FR&smc=1&dep=0&tn='+str(train_number)+'&tr=00:00-60&stn=1&pid=ssid').read()
    soup = BeautifulSoup.BeautifulSoup(html)

    tab = soup.find('div', attrs={"class": "TrainScrollPanel", "id": "M_C_TrainPanel_TrainStopsPanel"}).find('table')

    data = []

    for tr in tab.findAll('tr'):
        line = {}
        info = None
        try:
            info = tr.find('td', attrs={"class":"TrainColumnStationPast"}).find('a').string
        except:
            try:
                info = tr.find('td', attrs={"class":"TrainColumnStation"}).find('a').string
            except:
                info = None

        line["station"] = clean_string(info)
        info = None

        try:
            info = tr.find('td', attrs={"class":"TrainColumnArrivalPast"}).string
        except:
            try:
                info = tr.find('td', attrs={"class":"TrainColumnArrival"}).string
            except:
                info = None

        line["arrival"] = clean_string(info)
        info = None

        try:
            info = tr.find('td', attrs={"class":"TrainColumnArrivalDelayPast"}).string
        except:
            try:
                info = tr.find('td', attrs={"class":"TrainColumnArrivalDelay"}).string
            except:
                info = None

        line["arrival_delay"] = clean_string(info)
        info = None

        try:
            info = tr.find('td', attrs={"class":"TrainColumnDeparturePast"}).string
        except:
            try:
                info = tr.find('td', attrs={"class":"TrainColumnDeparture"}).string
            except:
                info = None

        line["departure"] = clean_string(info)
        info = None

        try:
            info = tr.find('td', attrs={"class":"TrainColumnDepartureDelayPast"}).string
        except:
            try:
                info = tr.find('td', attrs={"class":"TrainColumnDepartureDelay"}).string
            except:
                info = None

        line["departure_delay"] = clean_string(info)
        info = None

        data.append(line)
    return data

if __name__ == '__main__':
    j = []
    for i in range(906, 922):
        j.append(parse_train_data(i))
    # Write the Json
    file_name = strftime("Tournai-Mons_%d-%m-%Y_%H:%M:%S", gmtime())+'.json'
    with open(file_name, 'w') as f:
        f.write(json.dumps(j, indent=4, separators=(',', ': '),
                            sort_keys=True, ensure_ascii=False))
    j = []
    for i in range(928, 944):
        j.append(parse_train_data(i))
    # Write the Json
    file_name = strftime("Mons-Tournai_%d-%m-%Y_%H:%M:%S", gmtime())+'.json'
    with open(file_name, 'w') as f:
        f.write(json.dumps(j, indent=4, separators=(',', ': '),
                            sort_keys=True, ensure_ascii=False))
