import numpy as np
class Runner:
    def __init__(self, id, events, gender, age):
        self.id = id
        self.events = sorted(events, key = lambda x: x.date, reverse=True)
        # 0 = male, 1 = female
        self.gender = gender
        self.age = age

    def get_id(self):
        return self.id

    def get_gender(self):
        return self.gender

    def get_age(self):
        return self.age

    def get_total_races(self):
        return len(self.events)

    def get_event(self, event_name, event_year):
        try:
            # to get "Marathon Oasis de Montreal" in 2014, get_event("Oasis", "2014") would suffice just to prevent long strings
            return filter(lambda x: event_name in x.name and x.date[:4] == event_year, self.events)[0]
        except:
            # no participation == None
            return None

    def get_latest_event(self):
        return self.events[-1]

    def get_all_events(self):
        splitter =  "----------------------------------------"
        for e in self.events:
            print(splitter)
            print("Date: {}\n Name: {}\n Type: {}\n Time: {}\n Category: {}\n".format(e.date, e.name, e.etype, e.time, e.category))
        print(splitter)

    def get_all_completed_events(self):
        for e in self.events:
            if e.has_completed():
                print("Date: {}\n Name: {}\n Type: {}\n Time: {}\n Category: {}\n".format(e.date, e.name, e.etype, e.time, e.category))

    def get_feature(self):
        null_event = np.array([0,0,0])
        mtl_2014 = self.get_event("Oasis", "2014")
        ota_2013 = self.get_event("Ottawa", "2013")
        bnq_2015 = self.get_event("Banque", "2015")
        mtl = np.array([mtl_2014.get_participation(), mtl_2014.get_successful_finish(), mtl_2014.get_time_in_seconds()]) if mtl_2014 else null_event
        ota = np.array([ota_2013.get_participation(), ota_2013.get_successful_finish(), ota_2013.get_time_in_seconds()]) if ota_2013 else null_event
        bnq = np.array([bnq_2015.get_participation(), bnq_2015.get_successful_finish(), bnq_2015.get_time_in_seconds()]) if bnq_2015 else null_event
        othr = np.array([self.get_gender(), self.get_age(), self.get_total_races()])
        feat =  np.concatenate([mtl, ota, bnq, othr])
        return feat
