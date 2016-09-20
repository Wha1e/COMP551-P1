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
            #  and x.date[:4] == event_year
            return filter(lambda x: event_name in x.name and x.date[:4] == event_year, self.events)
        except:
            # no participation == None
            return None

    def get_latest_event(self):
        return self.events[-1]

    def get_all_events(self):
        splitter =  "----------------------------------------"
        for e in self.events:
            print(splitter)
            print("Date: {}\n Name: {}\n Type: {}\n Time: {}\n Category: {}\n".format(e.date, e.name, e.type, e.time, e.category))
        print(splitter)

    def get_all_completed_events(self):
        for e in self.events:
            if e.has_completed():
                print("Date: {}\n Name: {}\n Type: {}\n Time: {}\n Category: {}\n".format(e.date, e.name, e.type, e.time, e.category))
