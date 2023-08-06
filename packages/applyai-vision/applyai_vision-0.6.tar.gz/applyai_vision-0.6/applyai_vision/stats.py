# ----------------------------------------------------------------------------------------------------
# --- Python_3 ---                                                             Stand: 21.03.2019 / LG
# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
import numpy as np
import json
import pandas as pd
import math
import time
import os

#print(pd.__name__)
#print(np.__name__)

class stats:
    def __init__(self):
        self.timespath = '../common/stats/times.txt'
        self.times = pd.DataFrame(columns=['starttime','endtime','cycletime','flag'])
        self.maxCycles = 10
        self.jsonpath = '../common/stats/stats.json'
        self.json_data = {}
        try: 
            self.times = pd.read_csv('../common/stats/times.txt')
        except:
            print('no times.txt file')

    def insertCycletime(self, flag):
        zeit = pd.Timestamp.now()
        if flag == 1: #insert starttime
            self.times = self.times.append({'starttime': zeit, 'flag': flag}, ignore_index=True)
        if flag == 2: #insert endtime
            self.times.at[self.times.index[-1], 'endtime']   = zeit
            self.times.at[self.times.index[-1], 'cycletime'] = (self.times.at[self.times.index[-1], 'endtime'] - self.times.at[self.times.index[-1], 'starttime']).total_seconds()
            self.times.at[self.times.index[-1], 'flag']      = flag

        #print(self.times)

    def updateCycletime(self):
        #print(self.times["cycletime"])
        cycleTime = self.times["cycletime"].tail(10).mean()
        data = self.json_data['Stats']
        for i in range(len(data)):
            #print(data[i]['name'])
            if data[i]['name'] == "cycleTime":
                data[i]['value'] = cycleTime
        self.times.to_csv('../common/stats/times.txt', index=False, float_format='%.3f')

    def cycleTime(self):
        #df = pd.read_csv(self.times)
        #print(df["time"].mean())
        df_ = pd.DataFrame(columns=['time'])
        df_.append({'time': 2}, ignore_index=True)
        #print(df_)

    def incrementDetection(self, n):
        #print(json_data['Stats'])
        data = self.json_data['Stats']
        for i in range(len(data)):
            #print(data[i]['name'])
            if data[i]['name'] == "nDetects":
                data[i]['value'] = str(int(data[i]['value']) + n)
                #print(data[i]['name'])
                #print(data[i]['value'])
        #print(self.json_data)

    def read(self):
        with open(self.jsonpath, 'r') as file:
            self.json_data = json.load(file)

    def write(self):
        data = json.dumps(self.json_data, indent=4, sort_keys=True)
        with open(self.jsonpath, 'w') as f:
            f.write(data)

if __name__ == "__main__":
    stats = stats()
    stats.read()
    incr = stats.incrementDetection(1)
    stats.cycleTime()
    stats.insertCycletime(1)
    time.sleep(2)
    stats.insertCycletime(2)
    stats.updateCycletime()
    stats.write()
    print("stats.py | end")
