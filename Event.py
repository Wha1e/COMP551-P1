import numpy as np
class Event:
    def __init__(self, date, name, etype, time, category):
        self.date = date
        self.name = name
        self.etype = etype
        self.time = time # save as string
        self.category = category

    def get_participation(self):
        return 1

    def get_successful_finish(self):
        if self.time == "-1":
            return 0
        else:
            return 1

    def get_time_in_seconds(self):
        if self.time != "-1":
            h, m, s = self.time.split(':')
            return (int(h) * 3600) + (int(m) * 60) + int(s)
        else:
            return 0

'''
from Runner import Runner
from Event import Event
e1 = Event("2014-09-28", "Marathon Oasis de Montreal", "Marathon", "2:03:05", "M40-45")
e2 = Event("2013-09-29", "Ottawa", "Marathon", "2:00:05", "M40-45")
e3 = Event("2015-09-27", "Banque Oasis de Montreal", "Demi-Marathon", "1:03:05", "M40-45")
e4 = Event("2013-08-01", "Marathon Oasis de Montreal", "Marathon", "1:03:05", "M40-45")
r = Runner(1, [e1,e2,e3,e4], 0, 24)
r.get_feature()
'''
