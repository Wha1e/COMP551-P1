class Event:
    def __init__(self, date, name, etype, time, category):
        self.date = date
        self.name = name
        self.etype = etype
        self.time = time
        self.category = category

    def has_completed(self):
        return self.time != -1


'''
mock data
from Runner import Runner
from Event import Event
e1 = Event("2014-09-28", "Marathon Oasis de Montreal", "Marathon", "2:03:05", "M40-45")
e2 = Event("2013-09-29", "Marathon Oasis de Montreal", "Marathon", "2:00:05", "M40-45")
e3 = Event("2012-09-27", "Marathon Oasis de Montreal", "Demi-Marathon", "1:03:05", "M40-45")
e4 = Event("2013-08-01", "Marathon Oasis de Montreal", "Marathon", "1:03:05", "M40-45")
r = Runner(1, [e1,e2,e3,e4], "M", 24)
'''
